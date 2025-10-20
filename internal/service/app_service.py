#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time: 2025/10/20
@Author: 744534984cwl@gmail
@File: app_service.py
"""
from dataclasses import dataclass
from uuid import uuid4, UUID

from flask_sqlalchemy import SQLAlchemy
from injector import inject

from internal.model import App


@inject
@dataclass
class AppService:
    db: SQLAlchemy

    def create_app(self) -> App:
        app = App(
            account_id=uuid4(),
            name="AI application",
            icon="icon",
            description="app descriptions"
        )
        self.db.session.add(app)
        self.db.session.commit()
        return app

    def get_app(self, id: UUID) -> App:
        app = self.db.session.query(App).get(id)
        return app

    def update_app(self, id: UUID) -> App:
        app = self.get_app(id)
        app.name = "change name"
        self.db.session.commit()
        return app

    def delete_app(self, id: UUID) -> App:
        app = self.get_app(id)
        self.db.session.delete(app)
        self.db.session.commit()
        return app
