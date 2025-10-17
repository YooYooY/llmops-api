#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/17
@Author: 744534984cwl@gmail
@File: test_app_handler.py
"""
import pytest
from flask.testing import FlaskClient

from pkg.response import HttpCode


class TestAppHandler:

    @pytest.mark.parametrize("query", [None, "Hello"])
    def test_completion(self, client: FlaskClient, query):
        resp = client.post("/app/completion", json={"query": query})

        print(resp.json)

        assert resp.status_code == 200

        if query is None:
            assert resp.json.get("code") == HttpCode.VALIDATE_ERROR
        else:
            assert resp.json.get("code") == HttpCode.SUCCESS
