#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/1
@Author: 744534984cwl@gmail
@File: ChatMessageHistories.py
"""

from dotenv import load_dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-3.5-turbo")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm


def get_session_history(session_id: str):
    return FileChatMessageHistory(f'./history_{session_id}.json')


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

while True:
    query = input("Human: ")
    if query == "q":
        break
    response = chain_with_memory.invoke(
        {"input": query},
        config={"configurable": {"session_id": "default"}}
    )
    print(response.content)
