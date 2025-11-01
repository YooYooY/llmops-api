#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/1
@Author: 744534984cwl@gmail
@File: MemoryChatMessageHistory.py
"""
from langchain_core.chat_history import InMemoryChatMessageHistory

chat_history = InMemoryChatMessageHistory()
chat_history.add_user_message("Hello")
chat_history.add_ai_message("Hello, What's the matter?")

print(chat_history.messages)
