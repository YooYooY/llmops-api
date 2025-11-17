#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: app_handler.py
"""
from dataclasses import dataclass
from uuid import UUID

from injector import inject
from langchain_openai import ChatOpenAI
from sqlalchemy import text

from internal.extension.database_extension import db
from internal.service import AppService, VectorStoreService
from internal.utils import WeaviateV4VectorStore
from pkg.response import success_message, fail_message

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.6)


@inject
@dataclass
class AppHandler:
    app_service: AppService

    def __init__(self):
        vector_store = WeaviateV4VectorStore()
        self.vector_store_service = VectorStoreService(vector_store, llm)

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

    def add_doc(self, app_id: UUID):
        return self.vector_store_service.add_doc(app_id)

    def search(self, app_id: UUID):
        return self.vector_store_service.search(app_id)

    def rag_search(self, app_id: UUID):
        return self.vector_store_service.rag_search(app_id)

    def del_doc(self, app_id: UUID):
        return self.vector_store_service.delete_doc(app_id)

    # def debug(self, app_id: UUID):
    #     """chat interface"""
    #     req = CompletionReq()
    #     if not req.validate():
    #         return validate_error_json(req.errors)
    #
    #     query = request.json.get("query")
    #
    #     history = get_session_history(app_id)
    #     limiter.trim(history)
    #
    #     response = chain_with_memory.invoke(
    #         {"input": query},
    #         config={"configurable": {"app_id": app_id}},
    #     )
    #
    #     return success_json({"content": response.content})

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
