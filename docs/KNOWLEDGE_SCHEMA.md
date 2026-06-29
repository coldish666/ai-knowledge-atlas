# Knowledge Schema

## KnowledgeNode

核心字段：

- `slug`：稳定 URL 标识，例如 `gradient-descent`。
- `title`：知识点标题。
- `layer`：0-9 的知识层级。
- `category`：知识分类，如“深度学习”。
- `difficulty`：`入门`、`中等`、`挑战`。
- `summary`：一句话解释。
- `definition`：严谨定义。
- `intuition`：适合初学者的直觉解释。
- `why_it_matters`：为什么重要。
- `math_form`、`formulas`：数学表达和公式列表。
- `code_example`：最小 Python / PyTorch 示例。
- `applications`：至少 3 个应用场景。
- `misconceptions`：至少 2 个常见误区。
- `prerequisites`、`next_topics`、`related_topics`：slug 关系。
- `tags`、`recommended_resources`、`self_check_questions`、`extension_questions`。

## 关系类型

- `prerequisite`：当前知识依赖的前置知识。
- `next`：学完当前知识后适合继续学习的内容。
- `related`：同概念簇、同应用链路或经常互相解释的知识。

## 编写规范

不要只写标题和一句简介。新增知识点必须能独立阅读，也必须能通过 slug 链接到其他知识点。
