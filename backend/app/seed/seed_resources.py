from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import KnowledgeNode, KnowledgeResource


def res(
    knowledge_slug: str,
    title: str,
    url: str,
    source: str,
    resource_type: str,
    authority_level: str = "A",
    difficulty: str = "beginner",
    language: str = "en",
    estimated_time: str = "30 min",
    description: str = "",
    why_recommended: str = "",
    tags: list[str] | None = None,
) -> dict:
    return {
        "knowledge_slug": knowledge_slug,
        "title": title,
        "url": url,
        "source": source,
        "resource_type": resource_type,
        "authority_level": authority_level,
        "difficulty": difficulty,
        "language": language,
        "estimated_time": estimated_time,
        "description": description or f"{source} resource for learning {title}.",
        "why_recommended": why_recommended or "权威来源，适合作为该知识点的继续学习入口。",
        "tags": tags or [],
    }


RESOURCE_SPECS = [
    res("vector", "Mathematics for Machine Learning", "https://mml-book.github.io/", "MML Book", "book", "S", "beginner", "en", "3 h", "机器学习数学基础教材，覆盖线性代数、概率和优化。", "适合作为向量、矩阵和优化概念的系统入口。", ["math", "linear-algebra"]),
    res("vector", "Essence of Linear Algebra", "https://www.3blue1brown.com/topics/linear-algebra", "3Blue1Brown", "video", "A", "beginner", "en", "2 h", "线性代数可视化课程。", "直觉非常强，适合建立向量和线性变换的图像感。", ["visual", "linear-algebra"]),
    res("matrix", "MIT 18.06 Linear Algebra", "https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/", "MIT OCW", "course", "S", "intermediate", "en", "10 h", "Gilbert Strang 的经典线性代数公开课。", "大学级权威课程，适合补齐矩阵分解与线性系统基础。", ["math", "matrix"]),
    res("probability-distribution", "MIT 6.041SC Probability", "https://ocw.mit.edu/courses/6-041sc-probabilistic-systems-analysis-and-applied-probability-fall-2013/", "MIT OCW", "course", "S", "intermediate", "en", "8 h", "概率系统分析公开课程。", "适合系统理解随机变量、分布和期望。", ["probability"]),
    res("probability-distribution", "CS229 Main Notes", "https://cs229.stanford.edu/main_notes.pdf", "Stanford CS229", "course", "S", "intermediate", "en", "3 h", "Stanford CS229 课程主讲义。", "机器学习概率建模和监督学习公式的权威课程讲义。", ["ml", "probability"]),
    res("gradient-descent", "D2L Optimization", "https://d2l.ai/chapter_optimization/index.html", "Dive into Deep Learning", "book", "S", "beginner", "en", "1 h", "动手学深度学习的优化章节。", "从机器学习训练角度解释梯度下降和优化器。", ["optimization"]),
    res("gradient-descent", "CS231n Optimization Notes", "https://cs231n.github.io/optimization-1/", "Stanford CS231n", "course", "S", "beginner", "en", "45 min", "神经网络优化入门讲义。", "把梯度、损失和参数更新讲得很清楚。", ["gradient", "optimization"]),
    res("cross-entropy", "PyTorch CrossEntropyLoss", "https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html", "PyTorch", "official_doc", "S", "beginner", "en", "20 min", "PyTorch 交叉熵损失官方 API。", "最直接连接公式和工程调用方式。", ["loss", "classification"]),
    res("cross-entropy", "D2L Softmax Regression", "https://d2l.ai/chapter_linear-classification/softmax-regression.html", "Dive into Deep Learning", "book", "S", "beginner", "en", "45 min", "Softmax 与交叉熵的教材章节。", "适合理解分类模型为什么常用交叉熵。", ["softmax", "loss"]),
    res("kl-divergence", "Deep Learning Book: Probability", "https://www.deeplearningbook.org/contents/prob.html", "Deep Learning Book", "book", "S", "intermediate", "en", "1 h", "深度学习教材的概率章节。", "解释 KL、熵和概率分布在深度学习中的作用。", ["kl", "probability"]),
    res("kl-divergence", "PyTorch KLDivLoss", "https://pytorch.org/docs/stable/generated/torch.nn.KLDivLoss.html", "PyTorch", "official_doc", "S", "intermediate", "en", "20 min", "KL 散度损失官方 API。", "有助于把 KL 从概念落到训练代码。", ["kl", "loss"]),
    res("linear-regression", "scikit-learn Linear Models", "https://scikit-learn.org/stable/modules/linear_model.html", "scikit-learn", "official_doc", "S", "beginner", "en", "45 min", "线性模型用户指南。", "官方文档覆盖线性回归、逻辑回归和正则化。", ["linear-model"]),
    res("linear-regression", "D2L Linear Regression", "https://d2l.ai/chapter_linear-regression/index.html", "Dive into Deep Learning", "book", "S", "beginner", "en", "1 h", "线性回归从零实现章节。", "适合理解从损失函数到训练循环的完整路径。", ["regression"]),
    res("logistic-regression", "scikit-learn Logistic Regression", "https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression", "scikit-learn", "official_doc", "S", "beginner", "en", "30 min", "逻辑回归官方用户指南。", "解释分类、正则化和 solver 选择。", ["classification"]),
    res("logistic-regression", "CS229 Supervised Learning", "https://cs229.stanford.edu/main_notes.pdf", "Stanford CS229", "course", "S", "intermediate", "en", "2 h", "监督学习和广义线性模型讲义。", "适合从概率角度理解逻辑回归。", ["supervised-learning"]),
    res("svm", "scikit-learn SVM User Guide", "https://scikit-learn.org/stable/modules/svm.html", "scikit-learn", "official_doc", "S", "intermediate", "en", "45 min", "SVM 官方用户指南。", "覆盖核函数、分类和回归用法。", ["svm"]),
    res("svm", "CS229 SVM Notes", "https://cs229.stanford.edu/main_notes.pdf", "Stanford CS229", "course", "S", "advanced", "en", "2 h", "CS229 中最大间隔分类器相关内容。", "适合理解 SVM 的拉格朗日对偶和核技巧。", ["kernel", "margin"]),
    res("decision-tree", "scikit-learn Decision Trees", "https://scikit-learn.org/stable/modules/tree.html", "scikit-learn", "official_doc", "S", "beginner", "en", "40 min", "决策树官方用户指南。", "解释划分准则、剪枝和可解释性。", ["tree"]),
    res("random-forest", "scikit-learn Random Forests", "https://scikit-learn.org/stable/modules/ensemble.html#forests-of-randomized-trees", "scikit-learn", "official_doc", "S", "intermediate", "en", "45 min", "随机森林官方用户指南。", "适合理解 bagging、特征随机性和泛化。", ["ensemble"]),
    res("kmeans", "scikit-learn K-Means", "https://scikit-learn.org/stable/modules/clustering.html#k-means", "scikit-learn", "official_doc", "S", "beginner", "en", "35 min", "K-Means 官方用户指南。", "覆盖算法假设、复杂度和实践注意事项。", ["clustering"]),
    res("pca", "scikit-learn PCA", "https://scikit-learn.org/stable/modules/decomposition.html#pca", "scikit-learn", "official_doc", "S", "intermediate", "en", "45 min", "PCA 官方用户指南。", "适合连接线性代数、降维和 sklearn 实现。", ["pca", "decomposition"]),
    res("overfit-underfit", "scikit-learn Model Selection", "https://scikit-learn.org/stable/model_selection.html", "scikit-learn", "official_doc", "S", "beginner", "en", "1 h", "模型选择和交叉验证官方文档。", "解释过拟合诊断、验证集和调参流程。", ["model-selection"]),
    res("regularization", "scikit-learn Regularized Linear Models", "https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification", "scikit-learn", "official_doc", "S", "intermediate", "en", "35 min", "Ridge/Lasso 等正则化线性模型文档。", "适合理解 L1/L2 正则化如何影响模型复杂度。", ["regularization"]),
    res("classification-metrics", "scikit-learn Model Evaluation", "https://scikit-learn.org/stable/modules/model_evaluation.html", "scikit-learn", "official_doc", "S", "beginner", "en", "1 h", "模型评估指标官方指南。", "分类指标、回归指标和评分 API 都在这里。", ["metrics"]),
    res("neuron", "MIT 6.S191 Introduction to Deep Learning", "https://introtodeeplearning.com/", "MIT", "course", "S", "beginner", "en", "2 h", "MIT 深度学习入门课程。", "适合从神经元和网络结构开始建立全局直觉。", ["deep-learning"]),
    res("mlp", "D2L Multilayer Perceptrons", "https://d2l.ai/chapter_multilayer-perceptrons/index.html", "Dive into Deep Learning", "book", "S", "beginner", "en", "1 h", "MLP 教材章节。", "包含从零实现和框架实现，适合动手。", ["mlp"]),
    res("activation-function", "Deep Learning Book", "https://www.deeplearningbook.org/", "Deep Learning Book", "book", "S", "intermediate", "en", "2 h", "深度学习经典教材。", "适合理解非线性、优化和深层网络表达能力。", ["activation"]),
    res("backpropagation", "CS231n Backpropagation Notes", "https://cs231n.github.io/optimization-2/", "Stanford CS231n", "course", "S", "intermediate", "en", "1 h", "反向传播和计算图讲义。", "用计算图方式解释链式法则，非常适合查漏补缺。", ["backprop"]),
    res("automatic-differentiation", "PyTorch Autograd Tutorial", "https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html", "PyTorch", "official_doc", "S", "beginner", "en", "30 min", "PyTorch 自动求导快速教程。", "直接展示 autograd 如何记录图并反传梯度。", ["autograd"]),
    res("pytorch-dataset", "PyTorch Data Tutorial", "https://pytorch.org/tutorials/beginner/basics/data_tutorial.html", "PyTorch", "official_doc", "S", "beginner", "en", "30 min", "Dataset 和 DataLoader 官方教程。", "适合掌握训练数据管线的标准写法。", ["pytorch", "data"]),
    res("pytorch-training-loop", "PyTorch Optimization Tutorial", "https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html", "PyTorch", "official_doc", "S", "beginner", "en", "35 min", "训练循环官方基础教程。", "覆盖 loss、backward、optimizer.step 和评估循环。", ["training-loop"]),
    res("pytorch-training-loop", "PyTorch Examples", "https://github.com/pytorch/examples", "PyTorch", "code", "S", "intermediate", "en", "1 h", "PyTorch 官方示例仓库。", "可以查看 MNIST、ImageNet 等标准训练脚手架。", ["github", "examples"]),
    res("cnn", "CS231n Convolutional Networks", "https://cs231n.github.io/convolutional-networks/", "Stanford CS231n", "course", "S", "beginner", "en", "1 h", "CNN 结构、卷积和池化讲义。", "视觉模型入门最权威的公开课程材料之一。", ["cnn", "vision"]),
    res("cnn", "D2L Convolutional Neural Networks", "https://d2l.ai/chapter_convolutional-neural-networks/index.html", "Dive into Deep Learning", "book", "S", "beginner", "en", "1 h", "CNN 教材章节。", "适合把卷积公式、代码和训练连起来。", ["cnn"]),
    res("resnet", "Deep Residual Learning for Image Recognition", "https://arxiv.org/abs/1512.03385", "arXiv", "paper", "S", "intermediate", "en", "1 h", "ResNet 原论文。", "残差连接和深层 CNN 的必读论文。", ["resnet", "paper"]),
    res("resnet", "torchvision Models", "https://pytorch.org/vision/stable/models.html", "PyTorch", "official_doc", "S", "beginner", "en", "35 min", "torchvision 预训练模型文档。", "可以查看 ResNet 等视觉模型的工程调用方式。", ["torchvision"]),
    res("unet", "U-Net Paper", "https://arxiv.org/abs/1505.04597", "arXiv", "paper", "S", "intermediate", "en", "1 h", "U-Net 原论文。", "理解编码器-解码器和 skip connection 分割结构的经典入口。", ["segmentation"]),
    res("attention", "Attention Is All You Need", "https://arxiv.org/abs/1706.03762", "arXiv", "paper", "S", "intermediate", "en", "1.5 h", "Transformer 原论文。", "Attention、Multi-Head Attention 和位置编码的源头论文。", ["attention", "transformer"]),
    res("self-attention", "The Illustrated Transformer", "https://jalammar.github.io/illustrated-transformer/", "Jay Alammar", "blog", "S", "beginner", "en", "45 min", "Transformer 可视化讲解。", "用图解释 Self-Attention，非常适合建立直觉。", ["visual", "transformer"]),
    res("self-attention", "D2L Attention Mechanisms", "https://d2l.ai/chapter_attention-mechanisms-and-transformers/index.html", "Dive into Deep Learning", "book", "S", "intermediate", "en", "1.5 h", "注意力和 Transformer 教材章节。", "公式、代码和模型结构都有。", ["attention"]),
    res("multi-head-attention", "Attention Is All You Need", "https://arxiv.org/abs/1706.03762", "arXiv", "paper", "S", "intermediate", "en", "1.5 h", "Transformer 原论文。", "多头注意力的正式定义来自这里。", ["multi-head-attention"]),
    res("position-encoding", "Annotated Transformer", "https://nlp.seas.harvard.edu/annotated-transformer/", "Harvard NLP", "code", "S", "intermediate", "en", "1.5 h", "带代码注释的 Transformer 实现。", "位置编码、注意力和训练过程都可直接读代码。", ["transformer", "code"]),
    res("transformer-encoder", "Hugging Face Transformers Docs", "https://huggingface.co/docs/transformers/index", "Hugging Face", "official_doc", "S", "beginner", "en", "45 min", "Transformers 官方文档。", "连接 Transformer 架构和现代模型库实践。", ["transformers"]),
    res("transformer-decoder", "Stanford CS224N", "https://web.stanford.edu/class/cs224n/", "Stanford", "course", "S", "intermediate", "en", "4 h", "自然语言处理公开课。", "适合从序列建模走向 Transformer 和语言模型。", ["nlp", "transformer"]),
    res("tokenizer", "Hugging Face Tokenizers Docs", "https://huggingface.co/docs/tokenizers/index", "Hugging Face", "official_doc", "S", "beginner", "en", "30 min", "Tokenizers 官方文档。", "理解 BPE、WordPiece 和 tokenizer 工程接口。", ["tokenizer"]),
    res("tokenizer", "Hugging Face LLM Course", "https://huggingface.co/learn/llm-course/chapter1/1", "Hugging Face", "course", "S", "beginner", "en", "1 h", "LLM 课程入门章节。", "从 tokenizer、模型调用到训练应用都有路径。", ["llm"]),
    res("language-model", "Hugging Face Language Modeling Task Guide", "https://huggingface.co/docs/transformers/tasks/language_modeling", "Hugging Face", "official_doc", "S", "beginner", "en", "45 min", "语言模型任务官方指南。", "适合理解 causal language modeling 的数据和训练流程。", ["language-modeling"]),
    res("language-model", "Language Models are Few-Shot Learners", "https://arxiv.org/abs/2005.14165", "arXiv", "paper", "S", "advanced", "en", "1.5 h", "GPT-3 代表论文。", "大规模语言模型能力涌现和 few-shot 学习的重要论文。", ["gpt", "paper"]),
    res("decoder-only-transformer", "The Illustrated GPT-2", "https://jalammar.github.io/illustrated-gpt2/", "Jay Alammar", "blog", "A", "beginner", "en", "45 min", "GPT-2 和 decoder-only Transformer 可视化文章。", "适合直观理解自回归生成结构。", ["gpt", "decoder-only"]),
    res("decoder-only-transformer", "BERT Paper", "https://arxiv.org/abs/1810.04805", "arXiv", "paper", "S", "intermediate", "en", "1 h", "BERT 论文。", "用于对比 encoder-only 与 decoder-only 架构差异。", ["bert", "transformer"]),
    res("pretraining", "Stanford CS25 Transformers United", "https://web.stanford.edu/class/cs25/", "Stanford", "course", "A", "intermediate", "en", "3 h", "Transformer 和基础模型专题课程。", "适合从预训练模型的演化角度继续学习。", ["foundation-models"]),
    res("instruction-tuning", "Training Language Models to Follow Instructions", "https://arxiv.org/abs/2203.02155", "arXiv", "paper", "S", "advanced", "en", "1 h", "InstructGPT 论文。", "指令微调和人类反馈对齐的代表论文。", ["instruction-tuning"]),
    res("lora", "LoRA Paper", "https://arxiv.org/abs/2106.09685", "arXiv", "paper", "S", "intermediate", "en", "1 h", "低秩适配原论文。", "参数高效微调必读论文。", ["lora", "peft"]),
    res("lora", "Hugging Face PEFT LoRA", "https://huggingface.co/docs/peft/en/package_reference/lora", "Hugging Face", "official_doc", "S", "beginner", "en", "35 min", "PEFT 中 LoRA 的官方接口文档。", "适合把 LoRA 概念落实到工程配置。", ["peft"]),
    res("rlhf", "Hugging Face TRL Docs", "https://huggingface.co/docs/trl/index", "Hugging Face", "official_doc", "S", "intermediate", "en", "45 min", "TRL 官方文档。", "覆盖 RLHF、PPO、DPO 等训练工具链。", ["rlhf"]),
    res("prompt-engineering", "Prompt Engineering Guide", "https://www.promptingguide.ai/", "DAIR.AI", "chinese_note", "A", "beginner", "en", "1 h", "Prompt 技巧和模式汇总。", "适合快速查阅 few-shot、CoT、RAG prompt 等模式。", ["prompt"]),
    res("model-evaluation", "HELM", "https://crfm.stanford.edu/helm/latest/", "Stanford CRFM", "course", "S", "intermediate", "en", "1 h", "Holistic Evaluation of Language Models。", "大模型评测体系的权威入口。", ["evaluation"]),
    res("model-evaluation", "lm-evaluation-harness", "https://github.com/EleutherAI/lm-evaluation-harness", "EleutherAI", "code", "A", "intermediate", "en", "1 h", "开源 LLM 评测工具。", "适合理解 benchmark 如何实际跑起来。", ["evaluation", "github"]),
    res("rag-embedding", "Sentence Transformers Documentation", "https://www.sbert.net/", "Sentence Transformers", "official_doc", "S", "beginner", "en", "45 min", "句向量模型官方文档。", "适合理解和实践语义 embedding。", ["embedding"]),
    res("rag-embedding", "OpenAI Embeddings Guide", "https://platform.openai.com/docs/guides/embeddings", "OpenAI", "official_doc", "A", "beginner", "en", "30 min", "Embedding API 使用指南。", "作为 embedding 工程接口和检索应用的参考。", ["embedding", "api"]),
    res("vector-database", "FAISS Wiki", "https://github.com/facebookresearch/faiss/wiki", "FAISS", "official_doc", "S", "intermediate", "en", "45 min", "FAISS 官方 Wiki。", "理解向量索引、ANN 检索和性能权衡。", ["vector-search"]),
    res("vector-database", "Pinecone Docs", "https://docs.pinecone.io/guides/get-started/overview", "Pinecone", "official_doc", "A", "beginner", "en", "35 min", "向量数据库产品文档。", "适合理解托管向量库的集合、索引和查询概念。", ["vector-db"]),
    res("document-chunking", "LangChain Text Splitters", "https://python.langchain.com/docs/concepts/text_splitters/", "LangChain", "official_doc", "A", "beginner", "en", "30 min", "文本切分概念文档。", "适合理解 chunk size、overlap 和结构化切分。", ["chunking"]),
    res("retrieval", "LangChain Retrieval Concepts", "https://python.langchain.com/docs/concepts/retrieval/", "LangChain", "official_doc", "A", "beginner", "en", "40 min", "检索概念文档。", "系统梳理 retriever、query 和 document 的关系。", ["retrieval"]),
    res("retrieval", "LlamaIndex Documentation", "https://docs.llamaindex.ai/", "LlamaIndex", "official_doc", "A", "beginner", "en", "45 min", "RAG 数据框架文档。", "适合理解索引、检索、合成回答的完整流程。", ["rag"]),
    res("reranking", "Cohere Rerank Docs", "https://docs.cohere.com/docs/reranking", "Cohere", "official_doc", "A", "intermediate", "en", "25 min", "Rerank API 文档。", "直观展示重排序在 RAG 管线中的位置。", ["rerank"]),
    res("rag-evaluation", "Ragas Documentation", "https://docs.ragas.io/", "Ragas", "official_doc", "A", "intermediate", "en", "45 min", "RAG 评测框架文档。", "覆盖 faithfulness、answer relevancy 和 context precision 等指标。", ["rag-evaluation"]),
    res("tool-use", "Hugging Face Agents Course", "https://huggingface.co/learn/agents-course/", "Hugging Face", "course", "S", "beginner", "en", "2 h", "Agent 入门课程。", "覆盖工具、规划和 Agent 应用基础。", ["agent"]),
    res("function-calling", "OpenAI Function Calling Guide", "https://platform.openai.com/docs/guides/function-calling", "OpenAI", "official_doc", "A", "beginner", "en", "35 min", "函数调用官方指南。", "适合理解 schema、参数和工具调用边界。", ["function-calling"]),
    res("agentic-rag", "ReAct Paper", "https://arxiv.org/abs/2210.03629", "arXiv", "paper", "S", "intermediate", "en", "1 h", "Reasoning and Acting 代表论文。", "Agentic RAG 中思考、检索、行动循环的关键思想来源。", ["react", "agent"]),
    res("tool-use", "Toolformer Paper", "https://arxiv.org/abs/2302.04761", "arXiv", "paper", "S", "advanced", "en", "1 h", "Toolformer 论文。", "展示语言模型如何学习调用外部工具。", ["tool-use"]),
    res("workflow", "LangGraph Documentation", "https://langchain-ai.github.io/langgraph/", "LangGraph", "official_doc", "A", "intermediate", "en", "1 h", "Agent 工作流图框架文档。", "适合理解状态图、节点、边和可恢复执行。", ["workflow"]),
    res("memory", "MemGPT Paper", "https://arxiv.org/abs/2310.08560", "arXiv", "paper", "A", "advanced", "en", "1 h", "长上下文和记忆管理论文。", "适合理解 Agent 记忆的系统设计问题。", ["memory"]),
    res("agent-evaluation", "AgentBench Paper", "https://arxiv.org/abs/2308.03688", "arXiv", "paper", "A", "intermediate", "en", "1 h", "Agent 评测基准论文。", "可作为任务成功率和工具使用能力评估参考。", ["agent-eval"]),
    res("fastapi", "FastAPI Documentation", "https://fastapi.tiangolo.com/", "FastAPI", "official_doc", "S", "beginner", "en", "1 h", "FastAPI 官方文档。", "构建 AI 服务 API 的首选参考。", ["api"]),
    res("docker", "Docker Documentation", "https://docs.docker.com/", "Docker", "official_doc", "S", "beginner", "en", "1 h", "Docker 官方文档。", "部署环境封装和镜像构建的权威入口。", ["deployment"]),
    res("onnx", "ONNX Documentation", "https://onnx.ai/onnx/", "ONNX", "official_doc", "S", "intermediate", "en", "45 min", "ONNX 官方文档。", "理解模型交换格式和算子图结构。", ["onnx"]),
    res("onnx", "ONNX Runtime Documentation", "https://onnxruntime.ai/docs/", "ONNX Runtime", "official_doc", "S", "intermediate", "en", "45 min", "ONNX Runtime 官方文档。", "适合学习跨平台推理部署。", ["inference"]),
    res("tensorrt", "NVIDIA TensorRT Documentation", "https://docs.nvidia.com/deeplearning/tensorrt/latest/", "NVIDIA", "official_doc", "S", "advanced", "en", "1 h", "TensorRT 官方文档。", "GPU 推理优化和 engine 构建的权威资料。", ["tensorrt"]),
    res("quantization", "PyTorch Quantization", "https://pytorch.org/docs/stable/quantization.html", "PyTorch", "official_doc", "S", "intermediate", "en", "45 min", "PyTorch 量化官方文档。", "适合理解动态量化、静态量化和 QAT。", ["quantization"]),
    res("model-serving", "NVIDIA Triton Inference Server", "https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/", "NVIDIA", "official_doc", "A", "advanced", "en", "1 h", "Triton 推理服务文档。", "适合学习多模型、多后端和高性能推理服务。", ["serving"]),
    res("model-serving", "BentoML Documentation", "https://docs.bentoml.com/", "BentoML", "official_doc", "A", "beginner", "en", "45 min", "模型服务框架文档。", "适合快速封装模型服务和部署。", ["serving"]),
    res("ai-for-science", "AlphaFold Nature Paper", "https://www.nature.com/articles/s41586-021-03819-2", "Nature", "paper", "S", "advanced", "en", "1 h", "AlphaFold 蛋白质结构预测论文。", "AI for Science 代表性突破。", ["science", "alphafold"]),
    res("ai-for-science", "AlphaFold Code", "https://github.com/google-deepmind/alphafold", "DeepMind", "code", "S", "advanced", "en", "1 h", "AlphaFold 官方代码仓库。", "适合查看 AI for Science 项目的工程结构。", ["github", "science"]),
    res("pinn", "Physics-informed Neural Networks", "https://arxiv.org/abs/1711.10561", "arXiv", "paper", "S", "advanced", "en", "1 h", "PINN 代表论文。", "理解物理残差如何进入神经网络损失。", ["pinn", "pde"]),
    res("neural-ode", "Neural Ordinary Differential Equations", "https://arxiv.org/abs/1806.07366", "arXiv", "paper", "S", "advanced", "en", "1 h", "Neural ODE 论文。", "连续深度模型和可微分 ODE 求解器的核心论文。", ["neural-ode"]),
    res("fourier-neural-operator", "Fourier Neural Operator", "https://arxiv.org/abs/2010.08895", "arXiv", "paper", "S", "advanced", "en", "1 h", "FNO 代表论文。", "神经算子和 PDE surrogate modeling 的重要入口。", ["fno"]),
    res("fourier-neural-operator", "NeuralOperator Code", "https://github.com/neuraloperator/neuraloperator", "NeuralOperator", "code", "A", "advanced", "en", "1 h", "神经算子开源代码库。", "适合动手复现实验和查看 FNO 实现。", ["github", "operator-learning"]),
    res("multimodal-llm", "LLaVA Paper", "https://arxiv.org/abs/2304.08485", "arXiv", "paper", "A", "intermediate", "en", "1 h", "视觉指令调优多模态模型论文。", "理解图文大模型训练流程的代表资料。", ["multimodal"]),
    res("multimodal-llm", "LLaVA Code", "https://github.com/haotian-liu/LLaVA", "LLaVA", "code", "A", "intermediate", "en", "1 h", "LLaVA 开源仓库。", "适合查看多模态模型数据、训练和推理脚本。", ["github", "multimodal"]),
    res("embodied-ai", "AI Habitat", "https://aihabitat.org/", "Meta AI", "official_doc", "A", "intermediate", "en", "1 h", "具身智能仿真平台。", "适合理解导航、交互和仿真环境。", ["embodied-ai"]),
    res("embodied-ai", "Berkeley Deep RL Course", "https://rail.eecs.berkeley.edu/deeprlcourse/", "UC Berkeley", "course", "S", "intermediate", "en", "5 h", "深度强化学习公开课。", "具身智能和控制方向的重要基础课程。", ["rl", "control"]),
    res("ai-safety-alignment", "NIST AI Risk Management Framework", "https://www.nist.gov/itl/ai-risk-management-framework", "NIST", "official_doc", "S", "intermediate", "en", "1 h", "AI 风险管理框架。", "AI 安全、治理和评测的权威政策技术入口。", ["safety"]),
    res("ai-safety-alignment", "Stanford Center for AI Safety", "https://aisafety.stanford.edu/", "Stanford", "course", "A", "intermediate", "en", "1 h", "AI 安全研究中心资源。", "适合跟进安全评测、对齐和风险研究方向。", ["alignment"]),
    res("mlp", "动手学深度学习中文版", "https://zh.d2l.ai/", "Dive into Deep Learning", "chinese_note", "S", "beginner", "zh", "2 h", "D2L 中文版。", "中文学习者最友好的深度学习教材入口。", ["中文", "deep-learning"]),
    res("self-attention", "Hugging Face LLM Course 中文", "https://huggingface.co/learn/llm-course/zh-CN/chapter1/1", "Hugging Face", "chinese_note", "A", "beginner", "zh", "1 h", "Hugging Face LLM 课程中文版本。", "适合中文阅读 Transformer 和 LLM 工程基础。", ["中文", "llm"]),
    res("rag-embedding", "LlamaIndex Chinese Docs", "https://docs.llamaindex.ai/en/stable/", "LlamaIndex", "chinese_note", "B", "beginner", "en", "45 min", "LlamaIndex 文档入口。", "虽然以英文为主，但结构清晰，适合 RAG 入门查阅。", ["rag"]),
]


FALLBACK_BY_LAYER = {
    0: ("Mathematics for Machine Learning", "https://mml-book.github.io/", "MML Book", "book", "S"),
    1: ("NumPy Documentation", "https://numpy.org/doc/stable/", "NumPy", "official_doc", "S"),
    2: ("scikit-learn User Guide", "https://scikit-learn.org/stable/user_guide.html", "scikit-learn", "official_doc", "S"),
    3: ("PyTorch Tutorials", "https://pytorch.org/tutorials/", "PyTorch", "official_doc", "S"),
    4: ("D2L Attention and Vision Chapters", "https://d2l.ai/", "Dive into Deep Learning", "book", "S"),
    5: ("Hugging Face LLM Course", "https://huggingface.co/learn/llm-course/chapter1/1", "Hugging Face", "course", "S"),
    6: ("LlamaIndex Documentation", "https://docs.llamaindex.ai/", "LlamaIndex", "official_doc", "A"),
    7: ("Hugging Face Agents Course", "https://huggingface.co/learn/agents-course/", "Hugging Face", "course", "S"),
    8: ("FastAPI Documentation", "https://fastapi.tiangolo.com/", "FastAPI", "official_doc", "S"),
    9: ("Papers with Code", "https://paperswithcode.com/", "Papers with Code", "code", "A"),
}


def seed_resources(db: Session) -> None:
    if db.scalar(select(KnowledgeResource).limit(1)) is not None:
        return

    nodes = list(db.scalars(select(KnowledgeNode)).all())
    known_slugs = {node.slug for node in nodes}
    seen: set[tuple[str, str]] = set()

    for spec in RESOURCE_SPECS:
        if spec["knowledge_slug"] not in known_slugs:
            continue
        key = (spec["knowledge_slug"], spec["url"])
        if key in seen:
            continue
        seen.add(key)
        db.add(KnowledgeResource(**spec))

    covered = {slug for slug, _url in seen}
    for node in nodes:
        if node.slug in covered:
            continue
        title, url, source, resource_type, authority_level = FALLBACK_BY_LAYER.get(node.layer, FALLBACK_BY_LAYER[9])
        db.add(
            KnowledgeResource(
                knowledge_slug=node.slug,
                title=title,
                url=url,
                source=source,
                resource_type=resource_type,
                authority_level=authority_level,
                difficulty="beginner",
                language="en",
                estimated_time="45 min",
                description=f"{source} 的通用权威学习入口，可作为「{node.title}」的延伸资料。",
                why_recommended="用于保证每个知识点都有可点击的继续学习资源；核心知识点会额外提供更精确的资源。",
                tags=[node.category, "fallback"],
            )
        )
    db.commit()
