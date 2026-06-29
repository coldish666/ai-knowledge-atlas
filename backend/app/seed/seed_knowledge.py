from sqlalchemy.orm import Session

from app.models import AppSettings, KnowledgeNode, KnowledgeRelation


LAYER_NAMES = {
    0: "数学与计算基础",
    1: "编程与数据处理",
    2: "经典机器学习",
    3: "深度学习",
    4: "核心模型家族",
    5: "大模型与生成式 AI",
    6: "RAG 与知识库",
    7: "AI Agent",
    8: "AI 工程化",
    9: "前沿方向",
}


TOPICS = [
    ("vector", "向量", 0, "数学与计算基础", "入门", ["线性代数", "表示"], "向量是一组有顺序的数，用来表示方向、大小或特征。", "v = [v1, v2, ..., vn]"),
    ("matrix", "矩阵", 0, "数学与计算基础", "入门", ["线性代数", "变换"], "矩阵是二维数字表，可表示线性变换、批量样本和模型参数。", "Y = XW + b"),
    ("tensor", "张量", 0, "数学与计算基础", "入门", ["线性代数", "深度学习"], "张量是向量和矩阵向更高维的推广，是深度学习框架中的核心数据结构。", "T ∈ R^(b×c×h×w)"),
    ("derivative-gradient", "导数与梯度", 0, "数学与计算基础", "入门", ["微积分", "优化"], "导数描述函数变化率，梯度把多变量函数每个方向的偏导组织成向量。", "∇f(x) = [∂f/∂x1, ..., ∂f/∂xn]"),
    ("chain-rule", "链式法则", 0, "数学与计算基础", "入门", ["微积分", "反向传播"], "链式法则说明复合函数的导数如何逐层相乘，是反向传播的数学基础。", "d f(g(x))/dx = f'(g(x))g'(x)"),
    ("probability-distribution", "概率分布", 0, "数学与计算基础", "入门", ["概率", "不确定性"], "概率分布描述随机变量可能取值及其概率，是机器学习处理不确定性的语言。", "∑x p(x)=1 或 ∫p(x)dx=1"),
    ("maximum-likelihood", "最大似然估计", 0, "数学与计算基础", "中等", ["概率", "统计学习"], "最大似然估计选择最能解释观测数据的模型参数。", "θ* = argmax_θ ∏ p(x_i|θ)"),
    ("cross-entropy", "交叉熵", 0, "数学与计算基础", "中等", ["信息论", "损失函数"], "交叉熵衡量真实分布和预测分布之间的编码代价，常用于分类损失。", "H(p,q) = -∑ p(x)log q(x)"),
    ("kl-divergence", "KL 散度", 0, "数学与计算基础", "中等", ["信息论", "分布距离"], "KL 散度衡量用一个分布近似另一个分布时损失的信息量。", "D_KL(P||Q)=∑P(x)log(P(x)/Q(x))"),
    ("gradient-descent", "梯度下降", 0, "数学与计算基础", "入门", ["优化", "训练"], "梯度下降沿损失函数下降最快的反方向迭代更新参数。", "θ_{t+1}=θ_t-η∇L(θ_t)"),
    ("convex-optimization-intuition", "凸优化直觉", 0, "数学与计算基础", "中等", ["优化", "损失函数"], "凸优化关注没有坏局部最优的目标形状，帮助理解优化问题难易。", "f(λx+(1-λ)y) ≤ λf(x)+(1-λ)f(y)"),
    ("numerical-stability", "数值稳定性", 0, "数学与计算基础", "中等", ["计算", "工程"], "数值稳定性关注浮点上溢、下溢和舍入误差对模型计算的影响。", "logsumexp(x)=m+log∑exp(x-m)"),
    ("numpy-array", "NumPy 数组", 1, "Python 与数据处理", "入门", ["Python", "数组"], "NumPy 数组提供高效的多维数值计算，是数据处理和模型原型的基础。", "X ∈ R^(n×d)"),
    ("pandas-dataframe", "Pandas DataFrame", 1, "Python 与数据处理", "入门", ["Python", "表格数据"], "DataFrame 用行列结构表达表格数据，适合清洗、聚合和探索分析。", "本知识点主要是工程概念，无核心公式；关注行、列、索引和类型。"),
    ("data-cleaning", "数据清洗", 1, "Python 与数据处理", "入门", ["数据工程", "质量"], "数据清洗处理缺失、异常、重复和类型问题，决定模型输入是否可信。", "本知识点主要是工程概念，无核心公式；核心是规则和质量检查。"),
    ("data-normalization", "数据标准化", 1, "Python 与数据处理", "入门", ["特征工程", "预处理"], "数据标准化把特征缩放到可比较范围，减少尺度差异对训练的干扰。", "z=(x-μ)/σ"),
    ("train-valid-test-split", "训练集验证集测试集", 1, "Python 与数据处理", "入门", ["评估", "数据划分"], "训练、验证、测试划分让模型开发、调参和最终评估互相隔离。", "D = D_train ∪ D_valid ∪ D_test"),
    ("data-leakage", "数据泄漏", 1, "Python 与数据处理", "中等", ["评估", "风险"], "数据泄漏指训练过程接触了本不该知道的信息，导致评估虚高。", "本知识点主要是工程概念，无核心公式；关注信息边界。"),
    ("visualization", "可视化", 1, "Python 与数据处理", "入门", ["EDA", "解释"], "可视化用图形发现分布、异常、趋势和模型错误模式。", "本知识点主要是工程概念，无核心公式；图形编码变量关系。"),
    ("sklearn-pipeline", "sklearn 基本流程", 1, "Python 与数据处理", "入门", ["sklearn", "流程"], "sklearn 流程把预处理、训练、预测和评估串成可复现的实验。", "ŷ = model.fit(X_train,y_train).predict(X_test)"),
    ("linear-regression", "线性回归", 2, "经典机器学习", "入门", ["监督学习", "回归"], "线性回归用特征的线性组合预测连续数值。", "ŷ = wᵀx + b"),
    ("logistic-regression", "逻辑回归", 2, "经典机器学习", "入门", ["监督学习", "分类"], "逻辑回归把线性打分经过 Sigmoid 转成二分类概率。", "p(y=1|x)=σ(wᵀx+b)"),
    ("knn", "KNN", 2, "经典机器学习", "入门", ["非参数", "分类"], "KNN 根据邻近样本投票或平均进行预测，核心假设是相近样本标签相近。", "ŷ = majority(y_i for x_i ∈ N_k(x))"),
    ("decision-tree", "决策树", 2, "经典机器学习", "入门", ["树模型", "可解释"], "决策树通过一系列特征条件切分样本空间。", "split* = argmax 信息增益"),
    ("random-forest", "随机森林", 2, "经典机器学习", "中等", ["集成学习", "树模型"], "随机森林训练多棵随机化决策树，再聚合降低方差。", "ŷ = mode(T_1(x),...,T_m(x))"),
    ("svm", "SVM", 2, "经典机器学习", "中等", ["间隔", "核方法"], "SVM 寻找最大化类别间隔的分类边界。", "min 1/2||w||² s.t. y_i(wᵀx_i+b)≥1"),
    ("kmeans", "KMeans", 2, "经典机器学习", "入门", ["聚类", "无监督"], "KMeans 通过迭代分配样本和更新中心寻找簇结构。", "min∑||x_i-μ_{c_i}||²"),
    ("pca", "PCA", 2, "经典机器学习", "中等", ["降维", "线性代数"], "PCA 寻找最大方差方向，把高维数据投影到低维空间。", "Z = XW_k"),
    ("overfit-underfit", "过拟合与欠拟合", 2, "经典机器学习", "入门", ["泛化", "诊断"], "过拟合是记住训练噪声，欠拟合是模型表达能力不足。", "generalization gap = train error - valid error"),
    ("regularization", "正则化", 2, "经典机器学习", "中等", ["泛化", "约束"], "正则化通过惩罚复杂度或注入噪声提升泛化。", "L_total = L_data + λΩ(θ)"),
    ("cross-validation", "交叉验证", 2, "经典机器学习", "中等", ["评估", "调参"], "交叉验证用多次训练/验证划分更稳定地估计模型表现。", "score = mean(score_k)"),
    ("classification-metrics", "分类评价指标", 2, "经典机器学习", "入门", ["评估", "分类"], "分类指标从准确率、精确率、召回率、F1 等角度衡量预测质量。", "F1 = 2PR/(P+R)"),
    ("neuron", "神经元", 3, "深度学习", "入门", ["神经网络", "基础"], "神经元对输入做加权求和并通过非线性函数输出。", "h = φ(wᵀx+b)"),
    ("mlp", "多层感知机", 3, "深度学习", "入门", ["神经网络", "MLP"], "多层感知机堆叠线性层和激活函数，拟合非线性映射。", "h_l = φ(W_l h_{l-1}+b_l)"),
    ("activation-function", "激活函数", 3, "深度学习", "入门", ["非线性", "训练"], "激活函数为网络引入非线性，使深层模型能表达复杂函数。", "ReLU(x)=max(0,x)"),
    ("backpropagation", "反向传播", 3, "深度学习", "中等", ["训练", "链式法则"], "反向传播用链式法则从输出层向前计算每个参数的梯度。", "∂L/∂W_l = ∂L/∂h_l · ∂h_l/∂W_l"),
    ("automatic-differentiation", "自动求导", 3, "深度学习", "中等", ["框架", "梯度"], "自动求导记录计算图并自动应用微分规则求梯度。", "grad = backward(computation_graph)"),
    ("loss-function", "损失函数", 3, "深度学习", "入门", ["目标函数", "训练"], "损失函数把模型输出和目标的差距转成可优化的标量。", "L = loss(y, ŷ)"),
    ("optimizer", "优化器", 3, "深度学习", "中等", ["训练", "优化"], "优化器根据梯度和状态决定参数更新方式，如 SGD、Adam。", "m_t=βm_{t-1}+(1-β)g_t"),
    ("batchnorm", "BatchNorm", 3, "深度学习", "中等", ["归一化", "稳定训练"], "BatchNorm 在小批量内标准化中间激活，改善训练稳定性。", "BN(x)=γ(x-μ_B)/√(σ_B²+ε)+β"),
    ("dropout", "Dropout", 3, "深度学习", "入门", ["正则化", "泛化"], "Dropout 训练时随机屏蔽神经元，降低特征共适应。", "h' = mask ⊙ h / p"),
    ("residual-connection", "残差连接", 3, "深度学习", "中等", ["深层网络", "梯度"], "残差连接让层学习增量 F(x)，缓解深层网络退化和梯度传递问题。", "y = F(x) + x"),
    ("pytorch-dataset", "PyTorch Dataset", 3, "深度学习", "入门", ["PyTorch", "数据"], "Dataset 封装样本读取逻辑，DataLoader 负责批处理和并行加载。", "sample = dataset[i]"),
    ("pytorch-training-loop", "PyTorch 训练循环", 3, "深度学习", "入门", ["PyTorch", "训练"], "训练循环按批次执行前向、损失、反向、优化和评估。", "loss.backward(); optimizer.step()"),
    ("convolution", "卷积", 4, "视觉模型", "入门", ["视觉", "局部模式"], "卷积用共享核在局部窗口提取空间模式。", "Y[i,j]=∑K[u,v]X[i+u,j+v]"),
    ("cnn", "CNN", 4, "视觉模型", "入门", ["视觉", "深度学习"], "CNN 通过卷积、非线性和池化逐层提取图像特征。", "feature_l = Conv_l(feature_{l-1})"),
    ("pooling", "池化", 4, "视觉模型", "入门", ["视觉", "降采样"], "池化压缩空间尺寸并提升局部平移鲁棒性。", "maxpool(X)=max window(X)"),
    ("resnet", "ResNet", 4, "视觉模型", "中等", ["视觉", "残差"], "ResNet 用残差块训练非常深的 CNN。", "y = F(x,{W_i}) + x"),
    ("unet", "U-Net", 4, "视觉模型", "中等", ["分割", "医学影像"], "U-Net 用编码器-解码器和跳连保留细节，常用于语义分割。", "mask = Decoder(Encoder(image), skips)"),
    ("vit", "ViT", 4, "视觉模型", "中等", ["视觉", "Transformer"], "ViT 把图像切成 patch 序列，用 Transformer 做视觉建模。", "tokens = Linear(patches) + pos"),
    ("object-detection", "目标检测", 4, "视觉模型", "中等", ["视觉", "定位"], "目标检测同时预测物体类别和边界框位置。", "output = {class, bbox, score}"),
    ("image-segmentation", "图像分割", 4, "视觉模型", "中等", ["视觉", "像素级"], "图像分割为每个像素预测类别或实例归属。", "mask ∈ {1..C}^{H×W}"),
    ("rnn", "RNN", 4, "序列模型与 Transformer", "中等", ["序列", "循环网络"], "RNN 用隐藏状态逐步处理序列，捕捉历史信息。", "h_t = φ(Wx_t + Uh_{t-1})"),
    ("lstm", "LSTM", 4, "序列模型与 Transformer", "中等", ["序列", "门控"], "LSTM 用门控和记忆单元缓解普通 RNN 的长期依赖问题。", "c_t = f_t⊙c_{t-1}+i_t⊙g_t"),
    ("embedding", "Embedding", 4, "序列模型与 Transformer", "入门", ["表示学习", "NLP"], "Embedding 把离散符号映射到连续向量空间。", "e_i = E[token_id]"),
    ("attention", "Attention", 4, "序列模型与 Transformer", "中等", ["注意力", "序列"], "Attention 让模型根据查询动态聚合最相关的信息。", "Attention(Q,K,V)=softmax(QKᵀ/√d)V"),
    ("self-attention", "Self-Attention", 4, "序列模型与 Transformer", "中等", ["注意力", "Transformer"], "Self-Attention 在同一序列内部计算 token 间依赖。", "A=softmax(QKᵀ/√d)V"),
    ("multi-head-attention", "Multi-Head Attention", 4, "序列模型与 Transformer", "中等", ["注意力", "Transformer"], "多头注意力并行学习不同关系子空间，再拼接融合。", "head_i=Attention(QW_i^Q,KW_i^K,VW_i^V)"),
    ("position-encoding", "Position Encoding", 4, "序列模型与 Transformer", "中等", ["位置", "Transformer"], "位置编码把顺序信息加入无循环的 Transformer。", "PE(pos,2i)=sin(pos/10000^(2i/d))"),
    ("transformer-encoder", "Transformer Encoder", 4, "序列模型与 Transformer", "中等", ["Transformer", "编码器"], "Transformer Encoder 通过自注意力和前馈网络生成上下文表示。", "x = FFN(MHA(x)+x)+x"),
    ("transformer-decoder", "Transformer Decoder", 4, "序列模型与 Transformer", "中等", ["Transformer", "解码器"], "Transformer Decoder 使用因果注意力逐 token 生成序列。", "p(x_t|x_<t)=softmax(W h_t)"),
    ("vae", "VAE", 5, "生成模型", "中等", ["生成模型", "概率"], "VAE 用潜变量和变分推断学习可采样的数据分布。", "ELBO = E_q log p(x|z) - KL(q(z|x)||p(z))"),
    ("gan", "GAN", 5, "生成模型", "中等", ["生成模型", "对抗训练"], "GAN 让生成器和判别器对抗学习逼近真实数据分布。", "min_G max_D E logD(x)+E log(1-D(G(z)))"),
    ("diffusion", "Diffusion", 5, "生成模型", "中等", ["生成模型", "扩散"], "Diffusion 通过逐步加噪和去噪学习生成数据。", "x_t = √α_t x_0 + √(1-α_t)ε"),
    ("score-matching", "Score Matching", 5, "生成模型", "挑战", ["生成模型", "概率梯度"], "Score Matching 学习数据分布对输入的梯度，即 score 函数。", "s_θ(x) ≈ ∇_x log p_data(x)"),
    ("flow-matching", "Flow Matching", 5, "生成模型", "挑战", ["生成模型", "连续流"], "Flow Matching 学习把噪声分布连续搬运到数据分布的速度场。", "dx/dt = v_θ(x,t)"),
    ("tokenizer", "Tokenizer", 5, "大模型 LLM", "入门", ["LLM", "文本处理"], "Tokenizer 把文本切成模型可处理的 token id。", "text → [token_id_1,...,token_id_n]"),
    ("language-model", "语言模型", 5, "大模型 LLM", "入门", ["LLM", "概率建模"], "语言模型估计文本序列的概率，常用下一个 token 预测训练。", "P(x)=∏P(x_t|x_<t)"),
    ("decoder-only-transformer", "Decoder-only Transformer", 5, "大模型 LLM", "中等", ["LLM", "Transformer"], "Decoder-only Transformer 用因果自注意力生成文本，是主流 LLM 架构。", "h_t = DecoderBlock(h_<t)"),
    ("pretraining", "预训练", 5, "大模型 LLM", "中等", ["LLM", "训练"], "预训练在大规模语料上学习通用语言和知识表示。", "min -∑logP(x_t|x_<t)"),
    ("instruction-tuning", "指令微调", 5, "大模型 LLM", "中等", ["LLM", "对齐"], "指令微调用指令-回答数据让模型更会遵循用户意图。", "min -logP(answer|instruction)"),
    ("lora", "LoRA", 5, "大模型 LLM", "中等", ["LLM", "高效微调"], "LoRA 通过低秩矩阵适配大模型权重，减少可训练参数。", "W' = W + BA"),
    ("rlhf", "RLHF", 5, "大模型 LLM", "挑战", ["LLM", "对齐"], "RLHF 用人类偏好训练奖励模型，再优化生成策略。", "max E[R(y)] - β KL(π||π_ref)"),
    ("prompt-engineering", "Prompt Engineering", 5, "大模型 LLM", "入门", ["LLM", "应用"], "Prompt Engineering 通过清晰上下文、约束和示例引导模型输出。", "本知识点主要是工程概念，无核心公式；核心是输入设计。"),
    ("hallucination", "幻觉问题", 5, "大模型 LLM", "中等", ["LLM", "可靠性"], "幻觉是模型生成看似可信但事实错误或无依据内容的现象。", "本知识点主要是可靠性概念，无核心公式；关注证据链。"),
    ("model-evaluation", "模型评测", 5, "大模型 LLM", "中等", ["LLM", "评估"], "模型评测用任务集、人工标准和自动指标衡量能力与风险。", "score = aggregate(metric_i)"),
    ("rag-embedding", "Embedding（RAG）", 6, "RAG 与知识库", "入门", ["RAG", "检索"], "RAG 中的 Embedding 把查询和文档片段映射到可比较的语义向量。", "sim(q,d)=q·d/(||q||||d||)"),
    ("vector-database", "向量数据库", 6, "RAG 与知识库", "中等", ["RAG", "索引"], "向量数据库存储向量并支持近似最近邻检索。", "top_k = ANN(query_vector)"),
    ("document-chunking", "文档切分", 6, "RAG 与知识库", "入门", ["RAG", "文本处理"], "文档切分把长文本拆成适合检索和上下文窗口的片段。", "chunks = split(text, size, overlap)"),
    ("retrieval", "检索", 6, "RAG 与知识库", "入门", ["RAG", "搜索"], "检索从知识库中找出与问题最相关的片段。", "D_k = top_k(score(q,d))"),
    ("reranking", "重排序", 6, "RAG 与知识库", "中等", ["RAG", "排序"], "重排序用更精细模型重新排列初检结果，提高引用质量。", "rank = sort(cross_encoder(q,d))"),
    ("context-window", "上下文窗口", 6, "RAG 与知识库", "入门", ["RAG", "LLM"], "上下文窗口限制模型一次能看到的 token 数，决定可放入多少证据。", "tokens(prompt + context) ≤ window_size"),
    ("citation-source", "引用来源", 6, "RAG 与知识库", "入门", ["RAG", "可信"], "引用来源把答案和证据片段连接起来，提升可追溯性。", "answer span ↔ source chunk"),
    ("rag-evaluation", "RAG 评测", 6, "RAG 与知识库", "中等", ["RAG", "评估"], "RAG 评测同时检查检索命中、答案正确性和引用可靠性。", "quality = f(retrieval, faithfulness, answer)"),
    ("agent-architecture", "Agent 基本结构", 7, "AI Agent", "入门", ["Agent", "架构"], "Agent 把模型、任务状态、工具和执行循环组合成可行动系统。", "Agent = LLM + tools + memory + policy"),
    ("tool-use", "工具调用", 7, "AI Agent", "入门", ["Agent", "工具"], "工具调用让模型把部分任务交给外部 API、函数或系统执行。", "tool_result = tool(args)"),
    ("function-calling", "Function Calling", 7, "AI Agent", "中等", ["Agent", "结构化输出"], "Function Calling 用结构化 schema 约束模型选择函数和参数。", "call = {name, arguments}"),
    ("planning", "规划", 7, "AI Agent", "中等", ["Agent", "推理"], "规划把复杂目标拆成可执行步骤，并在执行中更新路线。", "plan = [step_1,...,step_n]"),
    ("memory", "记忆", 7, "AI Agent", "中等", ["Agent", "状态"], "记忆保存对话、偏好、事实或工作状态，支持长期任务。", "memory_t = update(memory_{t-1}, event_t)"),
    ("workflow", "工作流", 7, "AI Agent", "入门", ["Agent", "流程"], "工作流用确定性节点和条件边组织 AI 系统执行过程。", "state_{t+1}=node_i(state_t)"),
    ("agentic-rag", "Agentic RAG", 7, "AI Agent", "中等", ["Agent", "RAG"], "Agentic RAG 让 Agent 主动检索、改写问题、验证证据并迭代回答。", "answer = agent(query, retrieve, verify)"),
    ("agent-evaluation", "Agent 评测", 7, "AI Agent", "中等", ["Agent", "评估"], "Agent 评测衡量任务完成率、工具正确性、成本和失败恢复能力。", "score = task_success - cost - risk"),
    ("fastapi", "FastAPI", 8, "工程化与部署", "入门", ["后端", "API"], "FastAPI 用 Python 类型提示快速构建高性能 API 服务。", "HTTP request → path operation → response"),
    ("gradio-streamlit", "Gradio / Streamlit", 8, "工程化与部署", "入门", ["Demo", "UI"], "Gradio 和 Streamlit 可快速搭建模型演示界面。", "本知识点主要是工程概念，无核心公式；关注交互与部署。"),
    ("docker", "Docker", 8, "工程化与部署", "入门", ["部署", "环境"], "Docker 把应用和依赖打包成一致运行的容器镜像。", "image = app + runtime + dependencies"),
    ("onnx", "ONNX", 8, "工程化与部署", "中等", ["部署", "模型格式"], "ONNX 是跨框架模型交换格式，便于推理部署。", "model_graph = nodes + tensors + ops"),
    ("tensorrt", "TensorRT", 8, "工程化与部署", "挑战", ["推理加速", "NVIDIA"], "TensorRT 针对 NVIDIA GPU 优化模型推理图和算子。", "optimized_engine = build(onnx_model)"),
    ("quantization", "量化", 8, "工程化与部署", "中等", ["推理加速", "压缩"], "量化用低精度数值表示权重和激活，降低显存和提升速度。", "x_int = round(x / scale) + zero_point"),
    ("model-serving", "模型服务", 8, "工程化与部署", "中等", ["服务化", "部署"], "模型服务把模型封装为稳定、可扩展、可观测的在线接口。", "latency = queue + preprocess + inference + postprocess"),
    ("logging-monitoring", "日志与监控", 8, "工程化与部署", "入门", ["运维", "可靠性"], "日志与监控记录请求、错误、延迟和资源指标，帮助定位问题。", "SLO = successful_requests / total_requests"),
    ("ai-for-science", "AI for Science", 9, "前沿方向", "中等", ["科学智能", "前沿"], "AI for Science 用机器学习加速科学发现、模拟和实验设计。", "model: scientific state → prediction"),
    ("pinn", "PINN", 9, "前沿方向", "挑战", ["科学计算", "PDE"], "PINN 把物理方程残差加入损失函数训练神经网络。", "L = L_data + λ||N[u]||²"),
    ("neural-ode", "Neural ODE", 9, "前沿方向", "挑战", ["连续模型", "微分方程"], "Neural ODE 用神经网络表示连续时间动力系统的导数。", "dh/dt = f_θ(h,t)"),
    ("fourier-neural-operator", "Fourier Neural Operator", 9, "前沿方向", "挑战", ["神经算子", "PDE"], "FNO 在频域学习函数到函数的映射，适合 PDE 族解算。", "v' = F^{-1}(R·F(v))"),
    ("multimodal-llm", "多模态大模型", 9, "前沿方向", "中等", ["多模态", "LLM"], "多模态大模型联合处理文本、图像、音频或视频。", "h = fuse(text_tokens, image_tokens)"),
    ("embodied-ai", "具身智能", 9, "前沿方向", "挑战", ["机器人", "Agent"], "具身智能研究智能体如何在物理或仿真环境中感知、行动和学习。", "action_t = policy(observation_t, goal)"),
    ("world-model", "世界模型", 9, "前沿方向", "挑战", ["强化学习", "预测"], "世界模型学习环境动态，用内部模拟支持规划和决策。", "s_{t+1} ~ p_θ(s_{t+1}|s_t,a_t)"),
    ("ai-safety-alignment", "AI 安全与对齐", 9, "前沿方向", "中等", ["安全", "对齐"], "AI 安全与对齐关注模型目标、行为和人类价值的一致性。", "risk = capability × misalignment × exposure"),
]


EXPLICIT_RELATED = {
    "gradient-descent": ["backpropagation", "optimizer", "loss-function"],
    "embedding": ["tokenizer", "self-attention", "rag-embedding"],
    "self-attention": ["attention", "multi-head-attention", "transformer-encoder"],
    "transformer-encoder": ["vit", "decoder-only-transformer", "language-model"],
    "transformer-decoder": ["decoder-only-transformer", "language-model"],
    "rag-embedding": ["embedding", "vector-database", "retrieval"],
    "retrieval": ["document-chunking", "reranking", "citation-source"],
    "agentic-rag": ["retrieval", "agent-architecture", "rag-evaluation"],
    "diffusion": ["score-matching", "flow-matching", "multimodal-llm"],
    "pinn": ["ai-for-science", "neural-ode", "fourier-neural-operator"],
    "quantization": ["model-serving", "tensorrt", "onnx"],
}


RESOURCE_BY_CATEGORY = {
    "数学与计算基础": ["Mathematics for Machine Learning", "3Blue1Brown 线性代数", "Deep Learning Book 数学章节"],
    "Python 与数据处理": ["Python 官方教程", "NumPy 官方文档", "pandas User Guide"],
    "经典机器学习": ["Stanford CS229", "scikit-learn User Guide", "Hands-On Machine Learning"],
    "深度学习": ["Dive into Deep Learning", "PyTorch 官方教程", "Deep Learning Book"],
    "视觉模型": ["CS231n", "torchvision 教程", "U-Net / ResNet 原论文"],
    "序列模型与 Transformer": ["The Illustrated Transformer", "Attention Is All You Need", "Hugging Face NLP Course"],
    "生成模型": ["Deep Generative Models 课程", "Diffusion Models 综述", "VAE / GAN 原论文"],
    "大模型 LLM": ["Hugging Face LLM Course", "OpenAI Cookbook", "LLM Evaluation Guide"],
    "RAG 与知识库": ["LlamaIndex 文档", "LangChain RAG 指南", "FAISS 教程"],
    "AI Agent": ["Hugging Face Agents Course", "OpenAI Agents SDK 文档", "ReAct 论文"],
    "工程化与部署": ["FastAPI 官方文档", "Docker 文档", "ONNX Runtime 文档"],
    "前沿方向": ["Papers with Code", "Nature Machine Intelligence", "MLSys / NeurIPS 论文"],
}


def code_for(slug: str, title: str, layer: int) -> str:
    if layer in {3, 4, 5} or slug in {"pytorch-dataset", "pytorch-training-loop"}:
        return f"""```python
import torch

# {title}: 最小张量示例
x = torch.randn(4, 8)
w = torch.randn(8, 3)
y = x @ w
print("{title}", y.shape)
```"""
    if layer == 8:
        return f"""```python
# {title}: 工程概念通常从接口或配置开始
config = {{"component": "{slug}", "enabled": True}}
print(config)
```"""
    return f"""```python
import numpy as np

# {title}: 最小数值示例
x = np.array([1.0, 2.0, 3.0])
print("{title}", x.mean(), x.shape)
```"""


def build_node(spec: tuple, previous_by_category: dict[str, str], next_by_slug: dict[str, str]) -> KnowledgeNode:
    slug, title, layer, category, difficulty, tags, summary, math = spec
    prereq = []
    if category in previous_by_category:
        prereq.append(previous_by_category[category])
    elif layer > 0:
        prereq.append(TOPICS[max(0, layer - 1)][0])
    related = list(dict.fromkeys(EXPLICIT_RELATED.get(slug, []) + prereq[-1:]))
    next_topics = [next_by_slug[slug]] if slug in next_by_slug else []
    applications = [
        f"在学习 {LAYER_NAMES[layer]} 时用来组织核心概念。",
        f"在项目中帮助判断 {title} 相关方法是否适合当前数据和目标。",
        f"在阅读论文或调试模型时作为解释结果和定位问题的基础。",
    ]
    misconceptions = [
        f"误区：把「{title}」只当成名词记忆，而不理解它解决的问题。",
        f"误区：忽略它和前置知识、后续知识之间的依赖关系。",
    ]
    return KnowledgeNode(
        slug=slug,
        title=title,
        layer=layer,
        category=category,
        difficulty=difficulty,
        summary=summary,
        definition=f"{title} 的严格定义：{summary} 在 AI 知识体系中，它属于「{category}」，通常用于连接理论表达、算法实现和工程判断。",
        intuition=f"直觉上，可以把「{title}」看成解决某类 AI 问题的一块积木。先理解它输入什么、输出什么、改变了什么，再去看公式和代码会更稳。",
        why_it_matters=f"{title} 很重要，因为它会影响模型表达、训练稳定性、检索质量或系统可用性。理解它能帮助你从会调用工具前进到能解释和改造系统。",
        math_form=math,
        formulas=[math, "若本条是工程概念，公式部分强调输入、输出、约束和评价指标。"],
        code_example=code_for(slug, title, layer),
        applications=applications,
        misconceptions=misconceptions,
        prerequisites=prereq,
        next_topics=next_topics,
        related_topics=related,
        tags=list(dict.fromkeys(tags + [category, LAYER_NAMES[layer]])),
        recommended_resources=RESOURCE_BY_CATEGORY.get(category, ["Papers with Code", "课程讲义", "官方文档"]),
        self_check_questions=[
            f"请用一句话解释「{title}」解决什么问题。",
            f"「{title}」依赖哪些前置概念？如果缺失会在哪里卡住？",
            f"请写出一个最小例子，说明「{title}」的输入、输出和常见误区。",
        ],
        extension_questions=[
            f"如果把「{title}」放进真实项目，你会如何验证它是否有效？",
            f"它和 {', '.join(related[:2]) if related else '同层知识'} 有什么差异和联系？",
        ],
    )


def seed_knowledge(db: Session) -> None:
    db.add(
        AppSettings(
            id=1,
            user_name="AI 学习者",
            preferred_style="直觉版",
            llm_provider="mock",
            api_base_url="https://api.openai.com/v1",
            ai_enabled=True,
            max_rag_chunks=5,
        )
    )

    next_by_slug: dict[str, str] = {}
    by_category: dict[str, list[str]] = {}
    for slug, _title, _layer, category, *_rest in TOPICS:
        by_category.setdefault(category, []).append(slug)
    for slugs in by_category.values():
        for index, slug in enumerate(slugs[:-1]):
            next_by_slug[slug] = slugs[index + 1]

    previous_by_category: dict[str, str] = {}
    nodes: list[KnowledgeNode] = []
    for spec in TOPICS:
        node = build_node(spec, previous_by_category, next_by_slug)
        nodes.append(node)
        previous_by_category[spec[3]] = spec[0]
        db.add(node)
    db.flush()

    relations: set[tuple[str, str, str]] = set()
    known_slugs = {node.slug for node in nodes}
    for node in nodes:
        for target in node.prerequisites:
            if target in known_slugs:
                relations.add((node.slug, target, "prerequisite"))
        for target in node.next_topics:
            if target in known_slugs:
                relations.add((node.slug, target, "next"))
        for target in node.related_topics:
            if target in known_slugs and target != node.slug:
                relations.add((node.slug, target, "related"))

    for source, target, relation_type in relations:
        db.add(KnowledgeRelation(source_slug=source, target_slug=target, relation_type=relation_type))
    db.commit()
