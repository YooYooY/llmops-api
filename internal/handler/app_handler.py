#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: app_handler.py
"""
import os
from dataclasses import dataclass
from uuid import UUID

from flask import request
from injector import inject
from langchain_community.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy import text

from internal.exception import FailException
from internal.extension.database_extension import db
from internal.schema.app_schema import CompletionReq
from internal.service.app_service import AppService
from pkg.response import validate_error_json, success_message, fail_message, success_json


@inject
@dataclass
class AppHandler:
    app_service: AppService

    def ping(self):
        # return {"ping": "pong2"}
        raise FailException(message="异常")

    def check_database(self):
        try:
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return success_message("database connected")
        except Exception as e:
            return fail_message(str(e))

    def completion(self):
        """chat interface"""
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        query = request.json.get("query")

        prompt = ChatPromptTemplate.from_template("{query}")

        client = ChatOpenAI(
            model="gpt-3.5-turbo-16k",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE")
        )

        str_parser = StrOutputParser()

        # content = str_parser.invoke(client.invoke(prompt.invoke({"query": query})))
        chain = prompt | client | str_parser

        content = chain.invoke({"query": query})

        return success_json({"content": content})

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
