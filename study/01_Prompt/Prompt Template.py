#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/26
@Author: 744534984cwl@gmail
@File: Prompt Template.py
"""
from langchain_core.prompts import PromptTemplate, PipelinePromptTemplate

full_template = PromptTemplate.from_template(
    """{instruction}

{example}

{start}
"""
)

instruction_template = PromptTemplate.from_template("You are simulate {person}")

example_template = PromptTemplate.from_template(
    """below was an interact example:
    
Q:{example_q}
A:{example_a}
    """
)

start_template = PromptTemplate.from_template(
    """you are a real person now, please reply the user question:
    
Q: {input}
A:
"""
)

pipeline_prompt = PipelinePromptTemplate(
    final_prompt=full_template,
    pipeline_prompts=[
        ("instruction", instruction_template),
        ("example", example_template),
        ("start", start_template)
    ]
)

# print(pipeline_prompt)

pipeline_prompt_value = pipeline_prompt.invoke(
    {
        "person": "Wilbur",
        "example_q": "What's your favourite fruit?",
        "example_a": "Apple",
        "input": "What's your favorite Car?"
    }
)

print(pipeline_prompt_value.to_string())
