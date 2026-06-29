param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 5173,
    [switch]$NoBrowser,
    [int]$AutoStopAfterSeconds = 0
)

$ErrorActionPreference = "Stop"
$script:StartedProcessIds = @()
$script:ExitCode = 0

function Write-Step($Message) {
    Write-Host "[AI Knowledge Atlas] $Message" -ForegroundColor Cyan
}

function Get-Tool($Name) {
    $command = Get-Command $Name -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }
    return $null
}

function Get-Listener($Port) {
    $connection = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if (-not $connection) {
        return $null
    }

    $process = Get-CimInstance Win32_Process -Filter "ProcessId=$($connection.OwningProcess)" -ErrorAction SilentlyContinue
    [PSCustomObject]@{
        ProcessId = $connection.OwningProcess
        Name = if ($process) { $process.Name } else { "unknown" }
        CommandLine = if ($process) { $process.CommandLine } else { "" }
    }
}

function Clear-AppPort($Port, $Pattern, $Name) {
    $listener = Get-Listener $Port
    if (-not $listener) {
        return
    }

    $text = "$($listener.Name) $($listener.CommandLine)"
    if ($text -notmatch $Pattern) {
        throw "Port $Port is already used by $($listener.Name) (PID $($listener.ProcessId)). Close that program first."
    }

    Write-Step "Stopping previous $Name listener on port $Port..."
    & taskkill /PID $listener.ProcessId /T /F *> $null
    Start-Sleep -Seconds 1
}

function Stop-StartedProcesses {
    foreach ($processId in ($script:StartedProcessIds | Select-Object -Unique)) {
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($process) {
            Write-Step "Stopping process tree PID $processId..."
            & taskkill /PID $processId /T /F *> $null
        }
    }

    Clear-AppPort 5173 "vite|npm|node" "frontend"
    Clear-AppPort 8000 "uvicorn|app\.main:app|python" "backend"
}

function Wait-Url($Url, $Name, $Seconds) {
    for ($i = 0; $i -lt $Seconds; $i++) {
        try {
            $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 2
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                return
            }
        }
        catch {
            Start-Sleep -Seconds 1
        }
    }
    throw "$Name did not respond at $Url."
}

function Open-AppWindow($Url) {
    if ($NoBrowser) {
        return
    }

    $edgeCandidates = @(
        "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
        "${env:ProgramFiles}\Microsoft\Edge\Application\msedge.exe"
    )
    $edge = $edgeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($edge) {
        Start-Process -FilePath $edge -ArgumentList "--app=$Url" | Out-Null
        return
    }

    Start-Process $Url | Out-Null
}

function Wait-UntilUserCloses {
    Write-Host ""
    Write-Host "AI Knowledge Atlas is running locally without Docker." -ForegroundColor Green
    Write-Host "Frontend: http://127.0.0.1:$FrontendPort"
    Write-Host "Backend:  http://127.0.0.1:$BackendPort"
    Write-Host "Logs:     $script:LogsDir"
    Write-Host ""
    Write-Host "Keep this window open while using the app." -ForegroundColor Yellow
    Write-Host "Press Q or Enter in this window to stop frontend/backend automatically."
    Write-Host ""

    $startedAt = Get-Date
    $canReadKeys = $true
    try {
        $null = [Console]::KeyAvailable
    }
    catch {
        $canReadKeys = $false
    }

    while ($true) {
        if ($AutoStopAfterSeconds -gt 0 -and ((Get-Date) - $startedAt).TotalSeconds -ge $AutoStopAfterSeconds) {
            return
        }

        if ($canReadKeys -and [Console]::KeyAvailable) {
            $key = [Console]::ReadKey($true)
            if ($key.Key -in @("Q", "Enter", "Escape")) {
                return
            }
        }

        Start-Sleep -Milliseconds 300
    }
}

try {
    Register-EngineEvent PowerShell.Exiting -Action { Stop-StartedProcesses } | Out-Null

    $scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    $repoRoot = Resolve-Path (Join-Path $scriptRoot "..")
    $backendDir = Join-Path $repoRoot "backend"
    $frontendDir = Join-Path $repoRoot "frontend"
    $script:LogsDir = Join-Path $repoRoot "logs"
    $null = New-Item -ItemType Directory -Force -Path $script:LogsDir

    Write-Step "Preparing backend environment..."
    $python = Get-Tool "python"
    if (-not $python) {
        throw "Python was not found. Install Python 3.11+ and make sure python is in PATH."
    }

    $venvDir = Join-Path $backendDir ".venv"
    $venvPython = Join-Path $venvDir "Scripts\python.exe"
    if (-not (Test-Path $venvPython)) {
        Write-Step "Creating backend virtual environment..."
        & $python -m venv $venvDir
        if ($LASTEXITCODE -ne 0) {
            throw "Failed to create Python virtual environment."
        }
    }

    $backendEnv = Join-Path $backendDir ".env"
    $backendEnvExample = Join-Path $backendDir ".env.example"
    if (-not (Test-Path $backendEnv) -and (Test-Path $backendEnvExample)) {
        Copy-Item $backendEnvExample $backendEnv
    }

    $requirements = Join-Path $backendDir "requirements.txt"
    $pipStamp = Join-Path $venvDir ".requirements.stamp"
    $needsPipInstall = -not (Test-Path $pipStamp)
    if (-not $needsPipInstall -and (Get-Item $requirements).LastWriteTimeUtc -gt (Get-Item $pipStamp).LastWriteTimeUtc) {
        $needsPipInstall = $true
    }
    if ($needsPipInstall) {
        Write-Step "Installing backend dependencies..."
        & $venvPython -m pip install -r $requirements
        if ($LASTEXITCODE -ne 0) {
            throw "Backend dependency installation failed."
        }
        Set-Content -Path $pipStamp -Value (Get-Date).ToString("o")
    }

    Write-Step "Preparing frontend environment..."
    $npm = Get-Tool "npm.cmd"
    if (-not $npm) {
        $npm = Get-Tool "npm"
    }
    if (-not $npm) {
        throw "npm was not found. Install Node.js LTS and make sure npm is in PATH."
    }

    $frontendEnv = Join-Path $frontendDir ".env"
    if (-not (Test-Path $frontendEnv)) {
        Set-Content -Path $frontendEnv -Value "VITE_API_BASE_URL=http://localhost:$BackendPort"
    }

    $nodeModules = Join-Path $frontendDir "node_modules"
    $packageLock = Join-Path $frontendDir "package-lock.json"
    $npmStamp = Join-Path $frontendDir ".npm-install.stamp"
    $needsNpmInstall = -not (Test-Path $nodeModules) -or -not (Test-Path $npmStamp)
    if (-not $needsNpmInstall -and (Test-Path $packageLock) -and (Get-Item $packageLock).LastWriteTimeUtc -gt (Get-Item $npmStamp).LastWriteTimeUtc) {
        $needsNpmInstall = $true
    }
    if ($needsNpmInstall) {
        Write-Step "Installing frontend dependencies..."
        Push-Location $frontendDir
        & $npm install
        $npmExit = $LASTEXITCODE
        Pop-Location
        if ($npmExit -ne 0) {
            throw "Frontend dependency installation failed."
        }
        Set-Content -Path $npmStamp -Value (Get-Date).ToString("o")
    }

    Clear-AppPort $BackendPort "uvicorn|app\.main:app|python" "backend"
    Clear-AppPort $FrontendPort "vite|npm|node" "frontend"

    Write-Step "Starting backend..."
    $backendProcess = Start-Process -FilePath $venvPython `
        -ArgumentList @("-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "$BackendPort") `
        -WorkingDirectory $backendDir `
        -RedirectStandardOutput (Join-Path $script:LogsDir "backend.log") `
        -RedirectStandardError (Join-Path $script:LogsDir "backend-error.log") `
        -WindowStyle Hidden `
        -PassThru
    $script:StartedProcessIds += $backendProcess.Id

    Write-Step "Waiting for backend..."
    Wait-Url "http://127.0.0.1:$BackendPort/health" "Backend" 60

    Write-Step "Starting frontend..."
    $frontendProcess = Start-Process -FilePath $npm `
        -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1", "--port", "$FrontendPort") `
        -WorkingDirectory $frontendDir `
        -RedirectStandardOutput (Join-Path $script:LogsDir "frontend.log") `
        -RedirectStandardError (Join-Path $script:LogsDir "frontend-error.log") `
        -WindowStyle Hidden `
        -PassThru
    $script:StartedProcessIds += $frontendProcess.Id

    Write-Step "Waiting for frontend..."
    Wait-Url "http://127.0.0.1:$FrontendPort" "Frontend" 60

    Write-Step "Opening http://127.0.0.1:$FrontendPort"
    Open-AppWindow "http://127.0.0.1:$FrontendPort"

    Wait-UntilUserCloses
}
catch {
    $script:ExitCode = 1
    Write-Host ""
    Write-Host "Failed to start AI Knowledge Atlas local mode:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Check logs in the logs folder if a process started but did not respond."
}
finally {
    Write-Step "Stopping local services..."
    Stop-StartedProcesses
    Write-Host "AI Knowledge Atlas has stopped." -ForegroundColor Green
}

if ($script:ExitCode -ne 0 -and $AutoStopAfterSeconds -eq 0) {
    Read-Host "Press Enter to close"
}
exit $script:ExitCode
