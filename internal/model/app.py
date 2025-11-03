#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/20
@Author: 744534984cwl@gmail
@File: app.py
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    PrimaryKeyConstraint,
    Column,
    UUID,
    String,
    Text,
    DateTime,
    Index,
    text,
)

from internal.extension.database_extension import db


class App(db.Model):
    """AI application model"""

    __tablename__ = "app"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_app_id"),
        Index("idx_app_account_id", "account_id"),
    )

    id = Column(
        UUID, default=uuid4, nullable=False, server_default=text("uuid_generate_v4()")
    )
    account_id = Column(UUID, nullable=False)
    name = Column(
        String(255),
        default="",
        nullable=False,
        server_default=text("''::character varying"),
    )
    icon = Column(
        String(255),
        default="",
        nullable=False,
        server_default=text("''::character varying"),
    )
    description = Column(
        Text, default="", nullable=False, server_default=text("''::text")
    )
    status = Column(
        String(255),
        default="",
        nullable=False,
        server_default=text("''::character varying"),
    )
    updated_at = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(0)"),
        server_onupdate=text("CURRENT_TIMESTAMP(0)"),
    )
    created_at = Column(
        DateTime,
        default=datetime.now,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP(0)"),
    )
