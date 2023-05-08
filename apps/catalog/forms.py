# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AIS.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

# login and registration


class CatalogForm(FlaskForm):
    title = StringField('Title',
                        id='title',
                        validators=[DataRequired()])
    description = TextAreaField('Description',
                                id='description',
                                validators=[DataRequired()])
