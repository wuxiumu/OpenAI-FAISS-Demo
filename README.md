# OpenAI-FAISS-Demo · 本地知识库问答 Demo

> **OpenAI + FAISS** 本地向量检索问答示例，适合私有文档问答起步。

**定制：** 微信 **qingbao199101**（备注：知识库问答）｜ [wuxiumu@163.com](mailto:wuxiumu@163.com)

基于 OpenAI Embedding 与 FAISS 实现的本地知识库问答系统。

## ✨ 项目简介

该项目结合了 OpenAI 向量嵌入与 FAISS 相似度搜索，支持将本地的 PDF、Markdown、TXT 等文档转为向量，构建知识库，实现语义检索与问答。

可用于企业内训资料问答、AI 助手、知识管理等场景。

## 🔧 功能特点

- 支持 TXT / PDF / Markdown 批量导入
- 自动分块处理文本（防止 token 超限）
- 使用 OpenAI `text-embedding-3-small` 构建向量
- 基于 FAISS 实现高效相似度检索
- 支持控制台与 Streamlit Web UI 查询
- 支持中文文档与多段上下文拼接

## 📦 安装与环境准备

### 环境建议（macOS M1/M2）

- Python 3.10+
- pip / virtualenv
- 推荐使用 `pyenv` 安装 Python，避免系统冲突

### 安装依赖

```bash
git clone https://github.com/wuxiumu/OpenAI-FAISS-Demo.git
cd OpenAI-FAISS-Demo
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 设置 API Key

复制 `.env.example` → `.env`，填入 Key：

```
OPENAI_API_KEY=your-openai-api-key
```

```bash
bash scripts/smoke.sh   # 无 Key 也可：文件/语法检查
```



## 📁 使用方法

### 1. 添加知识文档

将你的 `.pdf`、`.md`、`.txt` 文件放入 `docs/` 目录。

### 2. 运行向量构建脚本

```bash
python ingest.py
```

将自动构建 FAISS 向量索引，并生成 `vector.index` 与 `sources.txt`。

### 3. 使用控制台查询

```bash
python main.py
```

### 4. 使用 Web UI（推荐）

```bash
streamlit run app.py
```

访问：http://localhost:8501

## 📷 示例界面

<img src="https://archive.biliimg.com/bfs/archive/f7a9df354aefad67be2cd1b4262d14cb5a718f0f.png"  referrerpolicy="no-referrer">

## 🧠 待扩展方向

- 文档上传即向量化
- 支持本地 LLM（如 Ollama、GPT4All）
- 添加多轮问答与记忆机制
- 支持向量去重与增量构建

## 📄 License

MIT License. 使用前请遵守 OpenAI API 使用政策。

## SEO 字段预留（产品页 HTML 统一生成时用）

| 字段 | 用途 |
|---|---|
| `seo_title` | `<title>` / OG title |
| `seo_description` | meta description |
| `canonical_url` | 规范 URL |
| `og_image` | 分享图 |
| `robots` | 如 `index,follow` |
| `json_ld_type` | SoftwareApplication / WebPage / FAQPage |
| `hreflang` | zh-CN / en |
| `site_name` | 白标品牌名 |

> **GEO ≠ 地理定位。** GEO = Generative Engine Optimization（生成式引擎优化），见下一节。

## GEO（生成式引擎优化）

面向 ChatGPT / Perplexity / Gemini 等生成式答案引擎的可引用结构：中文为主、双语关键词、事实摘要前置、FAQ 收尾。

### 关键词（中英）

- 中文：本地知识库, FAISS, RAG问答, 文档问答Demo
- English: local knowledge base, FAISS RAG, document QA demo

### 事实摘要

- 产品：OpenAI + FAISS 本地知识库问答 Demo。
- 适合：要私有文档问答的小团队。
- 交付：语料接入、界面、部署定制。
- 不做：开箱即企业级权限与审计全家桶。

### FAQ

**Q：这是什么？**  
A：见事实摘要「产品」。

**Q：如何定制？**  
A：微信 `qingbao199101`，备注项目名。

**Q：是否含密钥？**  
A：默认不含，自行配置。

## 定制合作

语料管道、权限、模型接入。加微信备注「知识库问答」。

---

## 联系方式

定制、演示或合作：

- 邮箱：[wuxiumu@163.com](mailto:wuxiumu@163.com)
- 微信：**qingbao199101**（添加请备注来意）

### 赞助支持

如果内容对你有帮助，欢迎自愿赞助。

| 微信赞赏码 | 支付宝收款码 |
|---|---|
| ![微信赞赏码](https://chiguashentan-test.oss-cn-beijing.aliyuncs.com/wxprogram/zan/20261002185236_31_227.png) | ![支付宝收款码](https://chiguashentan-test.oss-cn-beijing.aliyuncs.com/wxprogram/zan/20261002185309_32_227.jpg) |

