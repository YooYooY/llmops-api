#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/16
@Author: 744534984cwl@gmail
@File: app_schema.py
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CompletionReq(FlaskForm):
    query = StringField("query", validators=[
        DataRequired(message="please input the user question"),
        Length(max=200, message="the word can not maximum than 2000 characters")
    ])
