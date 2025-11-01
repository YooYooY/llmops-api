#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/1
@Author: 744534984cwl@gmail
@File: Chat_with_memory_stream.py
"""
import os

from dotenv import load_dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from utils.token_limiter import TokenLimiter

load_dotenv()
os.makedirs("./chat_history", exist_ok=True)

MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 3000

llm = ChatOpenAI(model=MODEL_NAME, streaming=True, temperature=0.6)
limiter = TokenLimiter(model_name=MODEL_NAME, max_tokens=MAX_TOKENS)

# ===============================
#  Prompt 模板
# ===============================
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who remembers past conversations."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm


# ===============================
#  memory system（FileChatMessageHistory）
# ===============================
def get_session_history(session_id: str):
    return FileChatMessageHistory(f"./chat_history/{session_id}.json")


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# ===============================
#  main circulate
# ===============================
session_id = "default"

print("💬 AI Chat Started! input 'q' exit\n")

while True:
    query = input("👤 You: ").strip()
    if query.lower() == "q":
        print("👋 bye！")
        break

    history = get_session_history(session_id)
    limiter.trim(history)  # ✅ limit the token

    print("🤖 AI: ", end="", flush=True)

    for event in chain_with_memory.stream(
            {"input": query},
            config={"configurable": {"session_id": session_id}},
    ):
        if hasattr(event, "content") and event.content:
            print(event.content, end="", flush=True)
    print("\n")
