#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: ChatPrompt concat.py
"""
from langchain_core.prompts import ChatPromptTemplate

system_chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Chatbot, reply my question, i am call {username}")
])

human_chat_prompt = ChatPromptTemplate.from_messages([
    ("human", "{query}")
])

chat_prompt = system_chat_prompt + human_chat_prompt

print(chat_prompt)

chat_prompt_value = chat_prompt.invoke({"username": "Wilbur", "query": "Hello"})
print(chat_prompt_value)
