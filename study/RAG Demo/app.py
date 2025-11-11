#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/10
@Author: 744534984cwl@gmail
@File: app.py
"""
import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

load_dotenv()

print("✅ Pinecone Key Loaded:", bool(os.getenv("PINECONE_API_KEY")))
print("✅ HF Token Loaded:", bool(os.getenv("HUGGINGFACEHUB_API_TOKEN")))

app = Flask(__name__)

embedding = HuggingFaceEndpointEmbeddings(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = PineconeVectorStore(
    embedding=embedding,
    index_name="llmops",
    namespace="dataset"
)


# add data interface
@app.route("/add", methods=["POST"])
def add_texts():
    try:
        """
        # query
        {
            "texts": [
                "Cats love sleeping in the sun.",
                "Dogs enjoy running in the park."
            ],
            "metadatas": [
                {"page": 1}, {"page": 2}
            ]
        }
        """
        data = request.json
        texts = data.get("texts", [])
        metadatas = data.get("metadata", [{} for _ in texts])

        docs = [
            Document(page_content=text, metadata=meta)
            for text, meta in zip(texts, metadatas)
        ]

        ids = vector_store.add_documents(docs)

        return jsonify({"status": "success", "ids": ids})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/query", methods=["POST"])
def query_text():
    # {"query": "I have a cat that loves napping all day."}
    try:
        data = request.json
        query = data.get("query")
        filter_condition = data.get("filter", None)

        results = vector_store.similarity_search_with_relevance_scores(
            query, k=3, filter=filter_condition
        )

        formatted = [
            {
                "text": doc.page_content,
                "score": score,
                "metadata": doc.metadata
            }
            for doc, score in results
        ]
        return jsonify({"results": formatted})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/rag-query", methods=["POST"])
def rag_query():
    data = request.json
    query = data.get("query")

    docs = vector_store.similarity_search(query, k=3, filter=None)
    context = "\n".join([d.page_content for d in docs])

    llm = ChatOpenAI(model="gpt-3.5-turbo")

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant.
    Use the following context to answer the question:
    {context}

    Question: {query}
    """)

    chain = prompt | llm

    response = chain.invoke({"context": context, "query": query})

    return jsonify({
        "query": query,
        "answer": response.content,
        "context": [d.page_content for d in docs]
    })


@app.route("/delete", methods=["DELETE"])
def delete_vectors():
    # {"ids": ["uuid-1"]}
    try:
        data = request.json
        ids = data.get("ids", [])
        vector_store.delete(ids)
        return jsonify({"status": "deleted", "ids": ids})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/")
def home():
    return jsonify({"status": "Pinecone RAG API is running!"})


if __name__ == "__main__":
    app.run(debug=True)
