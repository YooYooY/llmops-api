#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: app_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from flask import request
from injector import inject
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from sqlalchemy import text

from internal.extension.database_extension import db
from internal.schema.app_schema import CompletionReq
from internal.service.app_service import AppService
from internal.utils import TokenLimiter
from pkg.response import validate_error_json, success_message, fail_message, success_json

MODEL_NAME = "gpt-3.5-turbo"
MAX_TOKENS = 3000

llm = ChatOpenAI(model=MODEL_NAME, streaming=True, temperature=0.6)
limiter = TokenLimiter(model_name=MODEL_NAME, max_tokens=MAX_TOKENS)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who remembers past conversations."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

str_parser = StrOutputParser()

chain = prompt | llm | str_parser


def get_session_history(app_id: UUID):
    return FileChatMessageHistory(f"./storage/memory/chat_history_{app_id}.json")


chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


@inject
@dataclass
class AppHandler:
    app_service: AppService

    def ping(self):
        return {"ping": "pong2"}
        # raise FailException(message="异常")

    def check_database(self):
        try:
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return success_message("database connected")
        except Exception as e:
            return fail_message(str(e))

    def debug(self, app_id: UUID):
        """chat interface"""
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        query = request.json.get("query")

        history = get_session_history(app_id)
        limiter.trim(history)

        response = chain_with_memory.invoke(
            {"input": query},
            config={"configurable": {"session_id": app_id}},
        )

        return success_json({"content": response})

    def create_app(self):
        app = self.app_service.create_app()
        return success_message(f"application create success, id: {app.id}")

    def get_app(self, id: UUID):
        app = self.app_service.get_app(id)
        return success_message(f"query success, app name:{app.name}")

    def update_app(self, id: UUID):
        app = self.app_service.update_app(id)
        return success_message(f"update success, application name: {app.name}")

    def delete_app(self, id: UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"app delete success, app name: {app.name}")
