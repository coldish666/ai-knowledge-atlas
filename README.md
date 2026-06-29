# AI Knowledge Atlas / AI 学习知识索引

AI Knowledge Atlas 是一个 React/Vite + FastAPI 的 AI 知识索引系统。它用知识树、知识图谱、交互教材、RAG 问答和权威资源库，把 AI 从数学基础到大模型、Agent、工程化与前沿方向组织成可浏览、可搜索、可部署的知识地图。

## 功能概览

- 知识树：首页和 Tree 页面展示 AI 学习主干与可折叠枝干。
- 知识图谱：展示 `prerequisite`、`next`、`related` 三类复杂关系。
- 知识详情：三栏交互教材，包含定义、直觉解释、公式、代码、应用、误区、自测和关系导航。
- 权威资源库：按知识点索引官方文档、课程、教材、论文、代码和中文辅助资料，只保存链接与简介。
- RAG 问答：上传 Markdown / TXT 后按关键词检索，并返回引用片段。
- Mock AI 导师：无 API Key 也能运行，后续可接 OpenAI-compatible provider。

## 技术栈

- Frontend：React、Vite、TypeScript、CSS。
- Backend：Python 3.11+、FastAPI、SQLAlchemy、Pydantic。
- Database：默认 SQLite，支持通过 `DATABASE_URL` 切换 PostgreSQL。
- AI / RAG：Mock LLM provider、OpenAI-compatible provider 接口、Markdown/TXT 上传、关键词检索。
- Tooling：pytest、Docker、Render/Railway/VPS 部署配置。

## 本地开发

后端：

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

前端：

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

本地分离开发时，`frontend/.env` 使用：

```bash
VITE_API_BASE_URL=http://localhost:8000
```

访问地址：

- 前端：http://localhost:5173
- 后端：http://localhost:8000
- API 文档：http://localhost:8000/docs

## Windows 一键本地启动（不使用 Docker）

如果只在本机使用，可以直接双击项目根目录的：

```bat
start-local.bat
```

它会自动完成：

- 创建 `backend\.venv`。
- 安装后端 `requirements.txt`。
- 检查并安装前端 `node_modules`。
- 生成本地前端配置 `frontend\.env`，让 Vite 请求 `http://localhost:8000`。
- 启动 FastAPI 后端和 Vite 前端。
- 打开 `http://127.0.0.1:5173`。

启动窗口会保持打开。使用结束后，在这个窗口按 `Q` / `Enter`，或关闭这个启动窗口，脚本会自动停止本地前端和后端。日志保存在 `logs/` 目录。这个启动方式不依赖 Docker，但需要电脑已安装 Python 3.11+ 和 Node.js LTS。

## 生产构建

生产合并部署时，前端使用相对路径请求 `/api`，不要设置 `VITE_API_BASE_URL`。

```bash
cd frontend
npm install
npm run build

cd ../backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

FastAPI 会自动托管 `frontend/dist`：

- `GET /` 返回前端首页。
- `GET /assets/...` 返回 Vite 静态资源。
- `GET /api/...` 返回后端 API。
- 前端 SPA 路由刷新会 fallback 到 `index.html`，不会 404。
- `GET /health` 保留给部署平台健康检查。

如需自定义静态目录：

```bash
FRONTEND_DIST_DIR=/app/frontend/dist
```

## 环境变量

常用后端变量：

```bash
DATABASE_URL=sqlite:///../data/knowledge_atlas.db
DATA_DIR=../data
UPLOAD_DIR=../data/uploads
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
FRONTEND_DIST_DIR=../frontend/dist
LLM_PROVIDER=mock
OPENAI_BASE_URL=https://api.openai.com/v1
```

根目录提供了 [.env.example](./.env.example)，后端和前端也分别保留了 `backend/.env.example`、`frontend/.env.example`。真实配置应写入本地 `.env` 文件或部署平台环境变量，不要提交到 GitHub。

数据库：

- 默认不设置 `DATABASE_URL` 时使用 SQLite：`data/knowledge_atlas.db`。
- 设置 `DATABASE_URL` 后可切换 PostgreSQL，例如 `postgresql://user:password@host:5432/dbname`。
- Render/Railway 可能提供 `postgres://...`，应用会自动转换为 SQLAlchemy 可用格式。
- Seed 数据通过“表为空才插入”的方式初始化，不会在正常启动时重复插入。

上传目录：

- 默认保存到 `data/uploads`。
- 可通过 `UPLOAD_DIR` 修改。
- 目录不存在会自动创建。
- 云部署使用 SQLite 或本地上传时，需要配置持久化磁盘；更大规模部署建议改对象存储。

CORS：

- 本地分离开发默认允许 `http://localhost:5173` 和 `http://127.0.0.1:5173`。
- 线上前后端分离时设置 `CORS_ORIGINS=https://your-frontend.example`。
- 前后端合并部署为同源访问，通常不会遇到 CORS。

## Docker 运行

构建镜像：

```bash
docker build -t ai-knowledge-atlas .
```

运行容器：

```bash
docker run --rm -p 8000:8000 \
  -e DATA_DIR=/app/data \
  -e UPLOAD_DIR=/app/data/uploads \
  -v ai_knowledge_data:/app/data \
  ai-knowledge-atlas
```

访问：

- 应用首页：http://localhost:8000
- API：http://localhost:8000/api/knowledge
- 健康检查：http://localhost:8000/health

也可以使用：

```bash
docker compose up --build
```

## Render 部署

仓库已包含 `Dockerfile` 和 `render.yaml`。推荐用 Docker Web Service。

Blueprint 方式：

1. 将仓库推送到 GitHub。
2. 在 Render 选择 New Blueprint，指向该仓库。
3. Render 会读取根目录 `render.yaml`。
4. 确认持久化磁盘挂载到 `/app/data`。
5. 部署后访问 Render 分配的公网 URL。

手动 Web Service 方式：

- Runtime：Docker
- Build Command：Docker 服务不需要手写，Render 使用 `Dockerfile`
- Start Command：Docker 服务使用镜像内 CMD：`uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health Check Path：`/health`
- Environment Variables：
  - `DATA_DIR=/app/data`
  - `UPLOAD_DIR=/app/data/uploads`
  - `FRONTEND_DIST_DIR=/app/frontend/dist`
  - `LLM_PROVIDER=mock`
  - `CORS_ORIGINS=https://你的-render域名`
- Persistent Disk：
  - Mount Path：`/app/data`
  - SQLite 数据库和上传文件都在这里。

如果使用 Render PostgreSQL：

```bash
DATABASE_URL=<Render PostgreSQL Internal Database URL>
```

## Railway / VPS

Railway：

- 使用 Dockerfile 部署。
- 设置 `PORT` 由平台提供。
- 如果使用 Railway Volume，把 `DATA_DIR` 和 `UPLOAD_DIR` 指向挂载目录。
- 如果使用 Railway PostgreSQL，设置 `DATABASE_URL`。

VPS：

```bash
docker build -t ai-knowledge-atlas .
docker run -d --name atlas -p 80:8000 -v /srv/atlas-data:/app/data ai-knowledge-atlas
```

也可以用 Nginx 反向代理到容器的 `8000` 端口并配置 HTTPS。

## Vercel + Render 分离部署

如果前端部署到 Vercel、后端部署到 Render：

前端 Vercel 环境变量：

```bash
VITE_API_BASE_URL=https://your-render-service.onrender.com
```

后端 Render 环境变量：

```bash
CORS_ORIGINS=https://your-vercel-app.vercel.app
```

这种模式下，Vercel 只托管前端，Render 只托管 FastAPI API；上传文件和数据库仍在 Render 侧处理。

## GitHub 上传注意事项

上传前请确认只提交源码、文档和安全的示例配置。仓库已经通过 `.gitignore` 排除以下本地文件：

- `.env`、`.env.local`、真实 API Key。
- Python 虚拟环境：`.venv/`、`venv/`。
- 前端依赖和构建产物：`node_modules/`、`frontend/node_modules/`、`frontend/dist/`、`dist/`、`build/`。
- 本地数据库和上传资料：`*.db`、`*.sqlite`、`*.sqlite3`、`data/uploads/`。
- 日志、缓存、编辑器文件：`logs/`、`*.log`、`__pycache__/`、`.pytest_cache/`、`.idea/`、`.vscode/`。

首次上传 GitHub：

```bash
git init
git add .
git status --short
git commit -m "Initial commit: AI Knowledge Atlas"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

提交前建议运行：

```bash
git status --ignored --short
```

确认 `.env`、数据库、上传目录、日志和依赖目录都显示为 ignored，而不是 staged。

## 常见问题

前端刷新 404：

- 合并部署时由 FastAPI SPA fallback 解决。
- 如果分离部署到 Vercel，需要在 Vercel 使用 SPA rewrite 到 `/index.html`。

API 请求 localhost：

- 生产构建不要设置 `VITE_API_BASE_URL=http://localhost:8000`。
- 合并部署默认走相对路径 `/api`。
- 分离部署时把 `VITE_API_BASE_URL` 设置成真实后端公网 URL。

上传文件丢失：

- 容器文件系统通常是临时的。
- 使用 Docker volume、Render Persistent Disk、Railway Volume，或后续改对象存储。

SQLite 数据丢失：

- SQLite 文件默认在 `DATA_DIR`。
- 云部署必须持久化 `DATA_DIR`。
- 多实例部署建议使用 PostgreSQL。

CORS 报错：

- 前后端合并部署同源访问不会有 CORS。
- 分离部署时设置后端 `CORS_ORIGINS` 为前端公网域名，多个域名用逗号分隔。

## 测试

```bash
cd backend
pytest
```

```bash
cd frontend
npm run build
```

## 资源 API

- `GET /api/knowledge/{slug}/resources`
- `POST /api/knowledge/{slug}/resources`
- `GET /api/resources?type=&authority_level=&difficulty=&language=&layer=&q=`
- `GET /api/resources/recommended?slug=`
- `PUT /api/resources/{id}`
- `DELETE /api/resources/{id}`
