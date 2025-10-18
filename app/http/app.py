#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: app.py
"""
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from injector import Injector

from app.http.module import ExtensionModule
from config import Config
from internal.router import Router
from internal.server import Http

injector = Injector([ExtensionModule])
load_dotenv()

app = Http(
    __name__,
    router=injector.get(Router),
    config=Config(),
    db=injector.get(SQLAlchemy)
)

if __name__ == "__main__":
    app.run(debug=True)
