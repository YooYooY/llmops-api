#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/20
@Author: 744534984cwl@gmail
@File: sqlalchemy.py
"""
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy


class SQLAlchemy(_SQLAlchemy):

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
