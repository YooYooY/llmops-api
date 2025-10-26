#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: Prompt base.py
"""
from datetime import datetime

from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

prompt = PromptTemplate.from_template("Please talk a joke about {subject}")

print(prompt.format(subject="developer"))
prompt_value = prompt.invoke({"subject": "developer"})
print(prompt_value)
print(prompt_value.to_string())
print(prompt_value.to_messages())

print("=====")
chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a Chatbot, current time is: {now}"),
        MessagesPlaceholder("chat_history"),
        HumanMessagePromptTemplate.from_template("Please talk a joke about {subject}")
    ]
).partial(now=datetime.now())

chat_prompt_value = chat_prompt.invoke({
    "chat_history": [
        ("human", "Hello"),
        AIMessage("Hello"),
    ],
    "subject": "developer"
})

print(chat_prompt_value)
print(chat_prompt_value.to_string())
print(chat_prompt_value.to_messages())
