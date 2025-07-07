# app.py
import os
import faiss
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# 加载 API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@st.cache_resource
def load_faiss_index():
    return faiss.read_index("vector.index")

@st.cache_resource
def load_sources():
    with open("sources.txt", "r", encoding="utf-8") as f:
        return f.readlines()

def embed_query(query: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

def search(query, k=3):
    index = load_faiss_index()
    sources = load_sources()
    q_vec = embed_query(query)
    D, I = index.search(np.array([q_vec]), k=k)

    matched = []
    for idx in I[0]:
        file, chunk = sources[idx].strip().split("\t", 1)
        matched.append((file, chunk))
    return matched

def ask_gpt(context, query):
    prompt = f"根据以下内容回答问题：\n\n{context}\n\n问题是：{query}"
    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个知识库问答助手"},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content.strip()

# --- Streamlit 页面布局 ---
st.set_page_config(page_title="本地知识问答", layout="wide")
st.title("📚 本地知识库问答系统")
st.markdown("支持 PDF / Markdown / 文本，基于 FAISS + OpenAI")

query = st.text_input("请输入你的问题", placeholder="例如：OpenAI 是做什么的？")

if st.button("🔍 查询") and query:
    with st.spinner("向量检索中..."):
        results = search(query)

    context = "\n---\n".join([r[1] for r in results])

    with st.spinner("调用 GPT 回答中..."):
        answer = ask_gpt(context, query)

    st.subheader("🤖 GPT 回答")
    st.write(answer)

    with st.expander("🧩 匹配到的上下文"):
        for i, (file, chunk) in enumerate(results):
            st.markdown(f"**{i+1}. 来自文件：`{file}`**")
            st.markdown(f"> {chunk}")