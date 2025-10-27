#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/27
@Author: 744534984cwl@gmail
@File: Trace an application.py
"""
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


agent = create_agent(
    model="gpt-3.5-turbo-16k",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
content = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the weather in San Francisco?"}]}
)

print(content)
