#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/17
@Author: 744534984cwl@gmail
@File: conftest.py
"""
import pytest

from app.http.app import app


@pytest.fixture()
def client():
    app.config.update({
        "TESTING": True
    })
    with app.test_client() as client:
        yield client
