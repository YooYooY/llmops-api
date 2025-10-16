#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: http.py
"""
from flask import Flask

from config import Config
from internal.router import Router


class Http(Flask):
    """Http server engine"""

    def __init__(self, *args, router: Router, config: Config, **kwargs):
        super().__init__(*args, **kwargs)

        router.register_router(self)
        self.config.from_object(config)
