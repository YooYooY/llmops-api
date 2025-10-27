#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/27
@Author: 744534984cwl@gmail
@File: Callback.py
"""
import time
from typing import Any, Optional
from uuid import UUID

from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain_core.callbacks import BaseCallbackHandler, StdOutCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


class LLMOpsCallbackHandler(BaseCallbackHandler):
    start_time: float = 0

    def on_chat_model_start(
            self,
            serialized: dict[str, Any],
            messages: list[list[BaseMessage]],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[list[str]] = None,
            metadata: Optional[dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        print("***chat model start***")
        print("serialized=>", serialized)
        print("messages=>", messages)
        self.start_time = time.time()

    def on_llm_end(
            self,
            response: LLMResult,
            *,
            run_id: UUID,
            parent_run_id: UUID | None = None,
            **kwargs: Any
    ) -> Any:
        print("\n***chat model end***")
        print("response=>", response)
        print("consume=>", time.time() - self.start_time)


prompt = ChatPromptTemplate.from_template("{query}")
chat = ChatOpenAI(model="gpt-3.5-turbo")
str_parser = StrOutputParser()

chain = {"query": RunnablePassthrough()} | prompt | chat | str_parser

# content = chain.invoke("Hello, who you are?", config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]})

res = chain.stream("Hello, who you are?", config={"callbacks": [StdOutCallbackHandler(), LLMOpsCallbackHandler()]})
for i in res:
    print(i, flush=True, end="")
