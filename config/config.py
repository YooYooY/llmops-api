#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/16
@Author: 744534984cwl@gmail
@File: config.py
"""
import os
from typing import Any

from config.default_config import DEFAULT_CONFIG


def _get_env(key: str) -> Any:
    return os.getenv(key, DEFAULT_CONFIG.get(key))


def _get_bool_env(key: str) -> Any:
    value: str = _get_env(key)
    return value.lower() == "true" if value is not None else False


class Config:
    JSON_AS_ASCII = False

    def __init__(self):
        # WTF config
        self.WTF_CSRF_ENABLED = False

        # SQLAlchemy config
        self.SQLALCHEMY_DATABASE_URI = _get_env("SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(_get_env("SQLALCHEMY_POOL_SIZE")),
            "pool_recycle": int(_get_env("SQLALCHEMY_POOL_RECYCLE")),
        }
        self.SQLALCHEMY_ECHO = _get_bool_env("SQLALCHEMY_ECHO")
        self.JSON_AS_ASCII = False
