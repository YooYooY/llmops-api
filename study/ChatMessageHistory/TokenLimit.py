#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/11/1
@Author: 744534984cwl@gmail
@File: TokenLimit.py
"""
import tiktoken
from dotenv import load_dotenv
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

MAX_TOKENS = 300

load_dotenv()


def count_tokens(messages):
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    text = "".join(m.content for m in messages)
    return len(enc.encode(text))


def trim_history(history: FileChatMessageHistory):
    messages = history.messages
    while count_tokens(messages) > MAX_TOKENS and len(messages) > 2:
        messages.pop(0)
        messages.pop(0)

    # history.messages = messages
    # history.save() # type: ignore
    history.clear()
    for m in messages:
        history.add_message(m)

    remain_count = count_tokens(messages)
    print(f"✅trimming complete, remaining token count: {remain_count}")
    return remain_count


llm = ChatOpenAI(model="gpt-3.5-turbo", streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder("history"),
    ("human", "{input}")
])

chain = prompt | llm


def get_session_history(session_id: str):
    return FileChatMessageHistory(f'./history_{session_id}.json')


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

while True:
    query = input("Human: ")
    if query.strip().lower() == 'q':
        break

    session_id = "default"
    history = get_session_history(session_id)
    trim_history(history)

    print("AI: ", end="", flush=True)

    for event in chain_with_memory.stream(
            {'input': query},
            config={"configurable": {"session_id": session_id}}
    ):
        if isinstance(event, str):
            print(event, end="", flush=True)
        elif hasattr(event, "content"):
            print(event.content, end="", flush=True)
    print("")
