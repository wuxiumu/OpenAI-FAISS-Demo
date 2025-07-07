# main.py 问答主逻辑
import os
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_query(query: str):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    )
    return np.array(response.data[0].embedding, dtype=np.float32)

def load_sources():
    with open("sources.txt", "r", encoding="utf-8") as f:
        return f.readlines()

def search_and_ask(query: str):
    index = faiss.read_index("vector.index")
    query_vec = embed_query(query)
    D, I = index.search(np.array([query_vec]), k=3)

    contexts = []
    with open("sources.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for i in I[0]:
            file, chunk = lines[i].strip().split("\t", 1)
            contexts.append(chunk)

    context_text = "\n---\n".join(contexts)

    prompt = f"根据以下内容回答问题：\n\n{context_text}\n\n问题是：{query}"

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "你是一个知识库问答助手"},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content.strip()

if __name__ == "__main__":
    query = input("请输入问题：")
    answer = search_and_ask(query)
    print("\n📘 回答：", answer)