#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/11
@Author: 744534984cwl@gmail
@File: update_dimension.py
"""
import os

from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# 删除旧索引
try:
    pc.delete_index("llmops")
except:
    pass

# 创建新索引，维度改为 384
pc.create_index(
    name="llmops",
    dimension=384,
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)
print("✅ Created index 'llmops' with dimension=384")
