#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: http.py
"""
from flask import Flask

from config import Config
from internal.exception import CustomException
from internal.router import Router
from pkg.response import Response, json, HttpCode


class Http(Flask):
    """Http server engine"""

    def __init__(self, *args, router: Router, config: Config, **kwargs):
        super().__init__(*args, **kwargs)

        router.register_router(self)
        self.config.from_object(config)

        self.register_error_handler(Exception, self._error_handle)

    def _error_handle(self, error: Exception):
        if isinstance(error, CustomException):
            return json(Response(
                code=error.code,
                message=error.message,
                data=error.data if error.data is not None else {}
            ))

        return json(Response(code=HttpCode.FAIL, message=str(error), data={}))
