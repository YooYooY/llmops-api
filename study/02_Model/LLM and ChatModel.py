#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: LLM and ChatModel.py
"""

from datetime import datetime

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a Chatbot, current time is: {now}",
        ),
        ("human", "{query}"),
    ]
).partial(now=datetime.now())

chat = ChatOpenAI(model="gpt-3.5-turbo")

# ai_message = chat.invoke(prompt.invoke({
#     "query": "What time it is? please talk a joke about developer"
# }))
#
# print(ai_message.content)

# print("==== batch ===")

# ai_messages = chat.batch(
#     [
#         prompt.invoke({"query": "Hello, who you are?"}),
#         prompt.invoke({"query": "Please  talk a joke about developer"})
#     ]
# )
#
# for ai_message in ai_messages:
#     print(ai_message.content)
#     print("=================")

# print("==== stream ===")

ai_message = chat.stream(prompt.invoke({"query": "Please introduce about LLM simple for me"}))

for chunk in ai_message:
    print(chunk.content, flush=True, end="")
