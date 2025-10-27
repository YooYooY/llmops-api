#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/27
@Author: 744534984cwl@gmail
@File: RunnableParallel simple.py
"""

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


def retrieval(query: str):
    print(f"Retrival: {query}")
    return "I am Amy"


prompt = ChatPromptTemplate.from_template(
    """please answer the question base on the context

<context>
{context}
</context>

user question: {query}
"""
)

chat = ChatOpenAI(model="gpt-3.5-turbo")

str_parser = StrOutputParser()

chain = (
        RunnablePassthrough.assign(context=lambda x: retrieval(x["query"]))
        | prompt
        | chat
        | str_parser
)

content = chain.invoke({"query": "Hello, who I am"})
print(content)
