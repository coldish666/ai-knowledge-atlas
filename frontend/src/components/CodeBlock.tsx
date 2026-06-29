export default function CodeBlock({ code }: { code: string }) {
  const cleaned = code.replace(/^```python\n?/, "").replace(/```$/, "");
  return (
    <pre className="code-block">
      <code>{cleaned}</code>
    </pre>
  );
}
