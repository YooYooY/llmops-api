#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/1
@Author: 744534984cwl@gmail
@File: token_limiter.py
"""
import tiktoken
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.messages import BaseMessage


class TokenLimiter:
    """
       Automatically detect and prune message history to prevent exceeding the model's maximum token limit
    """

    def __init__(self, model_name: str = "gpt-3.5-tubo", max_tokens: int = 3000):
        self.max_tokens = max_tokens
        self.enc = tiktoken.encoding_for_model(model_name)

    def count_tokens(self, messages: list[BaseMessage]) -> int:
        """calculating the number of tokens in the history"""
        text = "".join(m.content for m in messages)
        return len(self.enc.encode(text))

    def trim(self, history: FileChatMessageHistory):
        """If the number of the tokens exceeds max tokens, delete the oldest conversation message"""
        messages = history.messages
        total_tokens = self.count_tokens(messages)

        if total_tokens <= self.max_tokens:
            return total_tokens

        print(f"⚠️ Token limit exceeded ({total_tokens} > {self.max_tokens}), trimming begins...")

        while self.count_tokens(messages) > self.max_tokens and len(messages) > 2:
            messages.pop(0)
            messages.pop(0)

        history.clear()
        for m in messages:
            history.add_message(m)

        remain_count = self.count_tokens(messages)
        print(f"✅trimming complete, remaining token count: {remain_count}")
        return remain_count
