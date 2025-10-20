#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/17
@Author: 744534984cwl@gmail
@File: module.py.py
"""
from injector import Module, Binder

from internal.extension.database_extension import db
from pkg.sqlalchemy import SQLAlchemy


class ExtensionModule(Module):
    def configure(self, binder: Binder) -> None:
        binder.bind(SQLAlchemy, db)
