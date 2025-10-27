#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/27
@Author: 744534984cwl@gmail
@File: Chain.py
"""
from typing import Any

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")

chat = ChatOpenAI(model="gpt-3.5-turbo")

parser = StrOutputParser()


class Chain:
    steps: list = []

    def __init__(self, steps) -> None:
        self.steps = steps

    def invoke(self, input: Any) -> Any:
        for step in self.steps:
            input = step.invoke(input)
            print(step)
            print(input)
            print("====")
        return input


chain = Chain([prompt, chat, parser])
content = chain.invoke({"query": "Hello, who are you?"})

print(content)
