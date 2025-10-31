#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/31
@Author: 744534984cwl@gmail
@File: SummaryBufferMemory.py
"""
from os import getenv
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class ConversationSummaryBufferMemory:
    def __init__(self, summary: str = '', chat_histories: list = []) -> None:
        self.max_tokens = 300
        self.chat_histories = chat_histories
        self.summary = summary
        self._client = OpenAI(
            api_key=getenv("OPENAI_API_KEY"), base_url=getenv("OPENAI_API_BASE")
        )

    @classmethod
    def get_num_tokens(cls, text: str) -> int:
        return len(text)

    def save_context(self, human_query: str, ai_content: str) -> None:
        self.chat_histories.append({"human": human_query, "ai": ai_content})
        tokens = self.get_num_tokens(self.get_buffer_string())

        if tokens > self.max_tokens:
            first_chat = self.chat_histories.pop(0)
            print("Summary generate")
            self.summary = self.summary_text(f"👨Human: {first_chat['human']}\n🤖AI: {first_chat['ai']}")
            print("Summary generate success:", self.summary)

    def get_buffer_string(self):
        buffer = ""
        for chat in self.chat_histories:
            buffer += f"""👨Human:{chat['human']}\n🤖AI:{chat['ai']}\n"""
        return buffer.strip()

    def summary_text(self, new_chat_message: str) -> str:
        m_prompt = f"""you are a powerful chatBot. Based on the conversation by the user, summarize the content and add it to the previously provided summary, then return a new summary.
        <example>
        Current summary: Humans ask AI for its opinion on AI. AI believes it is a force for good. New conversation content:
        
        Human: Why do you believe that artificial intelligence is a force for good?
        AI: Because artificial intelligence will help humanity reach its full potential. New summary: Humans will ask AI what it thinks of AI. AI believes it is a force for good because it will help humanity reach its full potential.
        </example>
        ====The following data is the actual content that needs to be processed====
        
        Current summary: {self.summary}
        New conversation content: {new_chat_message}
        Please help the user generate a new summary of the above information.
        """

        m_messages: Any = [
            {"role": "user", "content": m_prompt},
        ]
        m_response = self._client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=m_messages
        )
        return m_response.choices[0].message.content

    def load_memory_variables(self):
        buffer_string = self.get_buffer_string()
        return {
            "chat_history": f"Summary: {self.summary}\nhistory message:\n{buffer_string}\n"
        }


client = OpenAI(api_key=getenv("OPENAI_API_KEY"), base_url=getenv("OPENAI_API_BASE"))
memory = ConversationSummaryBufferMemory()

while True:
    query = input("Human: ")
    if query == "q":
        break

    memory_variables = memory.load_memory_variables()
    prompt = f"You are a powerful chatbot. Please solve problems based on the relevant context and the user's question. \n{memory_variables.get("chat_history")} \nuser question: {query}"
    print("prompt=>", prompt)
    messages: Any = [
        {"role": "user", "content": prompt},
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        stream=True
    )

    print("🤖AI: ", flush=True, end="")
    answer = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content is None:
            break
        answer += content
        print(content, flush=True, end="")
    print("")
    memory.save_context(query, answer)
