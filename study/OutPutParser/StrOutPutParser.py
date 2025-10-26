#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: StrOutPutParser.py
"""
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")

chat = ChatOpenAI(model="gpt-3.5-turbo")

output_parser = StrOutputParser()
content = output_parser.invoke(chat.invoke(prompt.invoke({"query": "hello, who you are?"})))

print(content)
