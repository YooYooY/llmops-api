#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/17
@Author: 744534984cwl@gmail
@File: default_config.py
"""
DEFAULT_CONFIG = {
    # wtf config
    "WTF_CSRF_ENABLED": "False",

    # SQLAlchemy config
    "SQLALCHEMY_DATABASE_URI": "",
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_ECHO": "True",
    "SQLALCHEMY_POOL_RECYCLE": 3600,
}
