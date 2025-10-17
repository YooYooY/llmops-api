#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/16
@Author: 744534984cwl@gmail
@File: http_code.py
"""
from enum import Enum


class HttpCode(str, Enum):
    SUCCESS = "success"
    FAIL = "fail"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    VALIDATE_ERROR = "validate_error"
