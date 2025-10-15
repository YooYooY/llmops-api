#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: router.py
"""
from dataclasses import dataclass

from flask import Flask, Blueprint
from injector import inject

from internal.handler import AppHandler


@inject
@dataclass
class Router:
    """router"""

    app_handler: AppHandler

    def register_router(self, app: Flask):
        """register router"""
        # 1.create a blueprint
        bp = Blueprint("llmops", __name__, url_prefix="")

        # 2. binding the url in the controller
        bp.add_url_rule("/ping", view_func=self.app_handler.ping)

        # 3. register the blueprint in the app
        app.register_blueprint(bp)
