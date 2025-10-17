#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/16
@Author: 744534984cwl@gmail
@File: response.py
"""
from dataclasses import field, dataclass
from typing import Any

from flask import jsonify

from .http_code import HttpCode


@dataclass
class Response:
    code: HttpCode = HttpCode.SUCCESS
    message: str = ""
    data: Any = field(default_factory=dict)


def json(res: Response = None):
    return jsonify(res), 200


def success_json(data: Any = None):
    return json(Response(data=data))


def fail_json(data: Any = None):
    return json(Response(code=HttpCode.FAIL, data=data))


def validate_error_json(errors: dict = None):
    if not errors:
        return json(Response(code=HttpCode.VALIDATE_ERROR, message="Unprocessable Entity", data={}))

    first_key = next(iter(errors))
    msg = errors[first_key][0] if errors.get(first_key) else ""

    return json(Response(code=HttpCode.VALIDATE_ERROR, message=msg, data=errors))


def message(code: HttpCode = None, msg: str = ""):
    return json(Response(code=code, message=msg, data={}))


def success_message(msg: str = ""):
    return message(code=HttpCode.SUCCESS, msg=msg)


def fail_message(msg: str = ""):
    return message(code=HttpCode.FAIL, msg=msg)


def not_found_message(msg: str = ""):
    return message(code=HttpCode.NOT_FOUND, msg=msg)


def unauthorized_message(msg: str = ""):
    return message(code=HttpCode.UNAUTHORIZED, msg=msg)


def forbidden_message(msg: str = ""):
    return message(code=HttpCode.FORBIDDEN, msg=msg)
