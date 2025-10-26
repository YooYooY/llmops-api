#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: JsonOutPutParser.py
"""
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()


class Joke(BaseModel):
    joke: str = Field(description="Joke")
    laughing_point: str = Field(description="laughing point")


json_parser = JsonOutputParser(pydantic_object=Joke)
# print(json_parser.get_format_instructions())
# print("====")

prompt = ChatPromptTemplate.from_template(
    "Please answer the question based on the user question. \n{format_instructions}\n{query}"
).partial(format_instructions=json_parser.get_format_instructions())

chat = ChatOpenAI(model="gpt-3.5-turbo")
result = json_parser.invoke(chat.invoke(prompt.invoke({"query": "please talke a joke about developer"})))

print(type(result))
print(result)
