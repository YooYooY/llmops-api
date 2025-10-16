#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: app_handler.py
"""
import os
from typing import Any

from flask import request
from openai import OpenAI


class AppHandler:
    """controller"""

    def ping(self):
        return {"ping": "pong2"}

    def completion(self):
        """chat interface"""
        query = request.json.get("query")

        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

        messages: list[Any] = [
            {"role": "system", "content": "你是openai开发的聊天机器人"},
            {"role": "user", "content": query}
        ]

        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=messages,
        )

        content = completion.choices[0].message.content

        return content
