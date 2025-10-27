#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/27
@Author: 744534984cwl@gmail
@File: RunnableParallel.py
"""
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

load_dotenv()

joke_prompt = ChatPromptTemplate.from_template("Please write a joke about {subject} ")
poem_prompt = ChatPromptTemplate.from_template("Please write a poem about {subject} ")

chat = ChatOpenAI(model="gpt-3.5-turbo")

str_parser = StrOutputParser()

joke_chain = joke_prompt | chat | str_parser
poem_chain = poem_prompt | chat | str_parser

# map_chain = RunnableParallel({"joke": joke_chain, "poem": poem_chain})
map_chain = RunnableParallel(joke=joke_chain, poem=poem_chain)

content = map_chain.invoke({"subject": "cat"})

print(content)
