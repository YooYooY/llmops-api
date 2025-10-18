#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/17
@Author: 744534984cwl@gmail
@File: module.py.py
"""
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Binder

from internal.extension.database_extension import db


class ExtensionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, db)
