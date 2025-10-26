#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: Prompt concat.py
"""
from langchain_core.prompts import PromptTemplate

prompt = (
        PromptTemplate.from_template("Please talk a joke about {subject}")
        + ", just let me smile"
        + "\nuse {language}"
)

prompt_value = prompt.invoke({
    "subject": "developer",
    "language": "Japanese"
})

print(prompt_value.to_string())
print(prompt_value.to_messages())
