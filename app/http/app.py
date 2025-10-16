#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/14
@Author: 744534984cwl@gmail
@File: app.py
"""
from dotenv import load_dotenv
from injector import Injector

from internal.router import Router
from internal.server import Http

injector = Injector()
load_dotenv()

app = Http(__name__, router=injector.get(Router))

if __name__ == "__main__":
    app.run(debug=True)
