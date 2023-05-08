# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AIS.us
"""

from apps import db


class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean)

    def __init__(self, content, completed=False):
        self.content = content
        self.completed = completed