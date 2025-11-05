#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/5
@Author: 744534984cwl@gmail
@File: 01_OpenAIEmbeddings.py
"""
import os

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

texts = [
    "Cats are very independent animals and love to nap.",
    "I enjoy listening to music at night; it helps me relax.",
    "Learning new skills is an important part of personal growth.",
    "My dog loves playing fetch in the park.",
    "Reading books makes me feel calm and inspired.",
    "I had a dream about flying in space last night.",
    "Cooking pasta with tomato sauce is my favorite dish.",
    "Technology is evolving faster than ever before.",
    "Meditation helps clear my mind and improves focus.",
    "Traveling allows me to experience new cultures and ideas."
]

metadatas = [{"page": i + 1} for i in range(len(texts))]

db = FAISS.from_texts(
    texts,
    embeddings,
    metadatas,
    relevance_score_fn=lambda distance: 1.0 / (1.0 + distance)
)

print(f"✅ Initial vector count: {db.index.ntotal}")

query = "I have a lazy cat that sleeps all day."

# results = db.similarity_search_with_score(query, k=3)
results = db.similarity_search_with_relevance_scores(query, k=3)

print("\n🔍 Similarity Search Results:")
for doc, score in results:
    print(f" -> Text: {doc.page_content}\n Score: {score}\n")

# ===============================
# add delete vector
# ===============================
print("🟢 Adding new text...")
new_ids = db.add_texts(["My cat is seven years old and still loves sleeping."])

print("New IDs:", new_ids)
print("Vector count after add:", db.index.ntotal)

print("🗑️ Deleting first vector...")
first_id = list(db.index_to_docstore_id.values())[0]
db.delete([first_id])
print("Vector count after delete:", db.index.ntotal)

# ===============================
#  Persistent Storage
# ===============================
store_path = "./cache"
os.makedirs(store_path, exist_ok=True)

print("\n💾 Saving FAISS index locally...")
db.save_local(store_path)

# ===============================
# load data and search
# ===============================
print("\n📂 Loading FAISS index from disk...")
new_db = FAISS.load_local(
    folder_path=store_path,
    embeddings=embeddings,
    allow_dangerous_deserialization=True
)

query2 = "Do you know any animals that like to sleep a lot?"
results2 = new_db.similarity_search_with_relevance_scores(query2, k=2)
print("\n🔁 Results from reloaded FAISS:")
for doc, score in results2:
    print(f"  → Text: {doc.page_content}\n    Score: {score}\n")
