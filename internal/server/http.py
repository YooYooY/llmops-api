#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: http.py
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config
from internal.exception import CustomException
from internal.model import App
from internal.router import Router
from pkg.response import Response, json, HttpCode


class Http(Flask):
    """Http server engine"""

    def __init__(
            self,
            *args,
            router: Router,
            config: Config,
            db: SQLAlchemy,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        router.register_router(self)
        self.config.from_object(config)
        # self.json.ensure_ascii = False
        self.register_error_handler(Exception, self._error_handle)
        db.init_app(self)
        with self.app_context():
            _ = App()
            db.create_all()

    def _error_handle(self, error: Exception):
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {}
            ))

        return json(Response(code=HttpCode.FAIL, message=str(error), data={}))
