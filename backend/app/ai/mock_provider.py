from app.ai.base import LLMProvider


class MockLLMProvider(LLMProvider):
    name = "mock"

    def generate(self, prompt: str, context: list[str] | None = None, style: str = "直觉版") -> str:
        context_text = "\n".join(context or [])
        style_hint = {
            "直觉版": "用类比和渐进解释先建立直觉。",
            "数学版": "突出变量、目标函数和公式含义。",
            "代码版": "强调最小可运行代码和输入输出。",
            "考试版": "整理定义、易错点和典型问法。",
            "项目应用版": "连接到真实项目流程和工程取舍。",
        }.get(style, "用清晰分层的方式解释。")
        if context_text:
            return (
                f"Mock AI 导师（{style}）：{style_hint}\n\n"
                f"问题：{prompt}\n\n"
                f"参考知识片段：{context_text[:900]}\n\n"
                "学习建议：先复述定义，再说出它解决什么问题，最后用一个最小例子验证自己是否真的理解。"
            )
        return (
            f"Mock AI 导师（{style}）：{style_hint}\n\n"
            f"围绕「{prompt}」，建议从定义、直觉、数学形式、代码例子、常见误区五层理解。"
        )
