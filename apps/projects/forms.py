# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AIS.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, DateField, IntegerField
from wtforms.validators import DataRequired


# login and registration


class ProjectForm(FlaskForm):
    name = StringField('Project name',
                       id='name',
                       validators=[DataRequired()])
    number = StringField('Project NO',
                         id='number',
                         validators=[DataRequired()])
    value = StringField('Project value',
                        id='value',
                        validators=[DataRequired()])
    picture = FileField('Picture', id='picture',
                        validators=[DataRequired()])


class ProjectDetailForm(FlaskForm):

    description = StringField('Description',
                              id='description',
                              validators=[DataRequired()])
    loa_start_date = DateField('Loa Start Date',
                               id='loa_start_date',
                               validators=[DataRequired()])
    loa_completion_date = DateField('Loa Completion Date',
                                    id='loa_completion_date',
                                    validators=[DataRequired()])
    ld_rate_per_delay = IntegerField('LD Rate Per Delay',
                                     id='ld_rate_per_delay',
                                     validators=[DataRequired()])


class ProjectProgressForm(FlaskForm):

    description = StringField('Description',
                              id='description',
                              validators=[DataRequired()])
    ss_start_date_1 = DateField('SS Start Date 1',
                                id='ss_start_date_1',
                                validators=[DataRequired()])
    ss_completion_date_1 = DateField('SS Completion Date 1',
                                     id='ss_completion_date_1',
                                     validators=[DataRequired()])
    ss_start_date_2 = DateField('SS Start Date 2',
                                id='ss_start_date_2',
                                validators=[DataRequired()])
    ss_completion_date_2 = DateField('SS Completion Date 2',
                                     id='ss_completion_date_2',
                                     validators=[DataRequired()])


class ProjectEventForm(FlaskForm):
    event_no = StringField('Event No',
                           id='phase',
                           validators=[DataRequired()])
    description = StringField('Description',
                              id='description',
                              validators=[DataRequired()])
    supporint_documents = StringField('Supporint Documents',
                                    id='supporint_documents',
                                    validators=[DataRequired()])
    start_date = DateField('Start Date',
                           id='start_date',
                           validators=[DataRequired()])
    end_date = DateField('End Date',
                           id='end_date',
                           validators=[DataRequired()])
