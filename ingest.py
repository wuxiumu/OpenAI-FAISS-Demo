# ingest.py 知识向量化
import os
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import fitz  # PyMuPDF
import markdown
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv() # 1. 导入环境变量
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DOC_DIR = "docs" # 2. 定义文档目录

def read_txt(path): # 3. 定义读取文本函数
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_md(path): # 4. 定义读取 Markdown 函数
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
        # return markdown.markdown(raw)  Markdown 渲染为 HTML，不利于语义处理
        text = re.sub(r'[`*_>#\-]+', '', raw)  # 简单去格式符
        return text

def read_pdf(path):# 5. 定义读取 PDF 函数
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def read_file(path):# 6. 定义读取文件函数
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".txt":
        return read_txt(path)
    elif ext == ".md":
        return read_md(path)
    elif ext == ".pdf":
        return read_pdf(path)
    else:
        return None

def split_text(text):# 7. 定义分割文本函数
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)

def get_embeddings(texts):# 8. 定义获取向量函数
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [np.array(e.embedding, dtype=np.float32) for e in response.data]

def get_embeddings_batched(texts, batch_size=100):# 9. 定义获取向量批处理函数
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        res = client.embeddings.create(model="text-embedding-3-small", input=batch)
        all_embeddings.extend(np.array(e.embedding, dtype=np.float32) for e in res.data)
    return all_embeddings

if __name__ == "__main__":
    all_chunks = []
    metadata = []

    for file in os.listdir(DOC_DIR):
        path = os.path.join(DOC_DIR, file)
        try:
            content = read_file(path)  # 2. 添加异常处理，避免单个文件影响全部流程
        except Exception as e:
            print(f"读取失败: {file}, 错误: {e}")
            continue
        if not content:
            print(f"跳过不支持的文件: {file}")
            continue

        chunks = split_text(content)
        all_chunks.extend(chunks)
        metadata.extend([file] * len(chunks))

    print(f"共分割出 {len(all_chunks)} 段文本，开始生成向量...")

    # embeddings = get_embeddings(all_chunks) 3. embedding 批处理最好分批处理避免超长输入
    embeddings = get_embeddings_batched(all_chunks, batch_size=100)
    dim = len(embeddings[0])    #4. 建议添加向量维度检查，避免添加失败
    if not all(len(e) == dim for e in embeddings):
        raise ValueError("Embedding 维度不一致，可能是部分生成失败")
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    faiss.write_index(index, "vector.index")

    # 保存分块文本及其来源文件名
    with open("sources.txt", "w", encoding="utf-8") as f:
        for i in range(len(all_chunks)):
            text = all_chunks[i].replace('\n', ' ')
            f.write(f"{metadata[i]}\t{text}\n")

    print("✅ 向量库构建完成。")