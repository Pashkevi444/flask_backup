# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AIS.us
"""

from apps import db


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2000))
    number = db.Column(db.String(2000))
    value = db.Column(db.String(2000))
    progress = db.Column(db.Numeric(100))
    manager = db.Column(db.Numeric(100))
    director = db.Column(db.Text)
    preview_picture = db.Column(db.String(2000))


    def __init__(self, name, value, number, preview_picture):
        self.name = name
        self.number = number
        self.value = value
        self.preview_picture = preview_picture


class ProjectsDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.Integer)
    description = db.Column(db.Text(2000))
    loa_start_date = db.Column(db.Date)
    loa_completion_date = db.Column(db.Date)
    ld_rate_per_delay = db.Column(db.Numeric(100))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, phase, description, loa_start_date, loa_completion_date, ld_rate_per_delay, project_id):
        self.phase = phase
        self.description = description
        self.loa_start_date = loa_start_date
        self.loa_completion_date = loa_completion_date
        self.ld_rate_per_delay = ld_rate_per_delay
        self.project_id = project_id


class ProjectsProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.Integer)
    description = db.Column(db.String(2000))
    ss_start_date_1 = db.Column(db.Date)
    ss_completion_date_1 = db.Column(db.Date)
    ss_start_date_2 = db.Column(db.Date)
    ss_completion_date_2 = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, phase, description, ss_start_date_1, ss_completion_date_1, ss_start_date_2, ss_completion_date_2,
                 project_id):
        self.phase = phase
        self.description = description
        self.ss_start_date_1 = ss_start_date_1
        self.ss_completion_date_1 = ss_completion_date_1
        self.ss_start_date_2 = ss_start_date_2
        self.ss_completion_date_2 = ss_completion_date_2
        self.project_id = project_id


class ProjectsDelayEvents(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_no = db.Column(db.String(2000))
    description = db.Column(db.String(2000))
    supporint_documents = db.Column(db.String(2000))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    def __init__(self, event_no, description, supporint_documents, start_date, end_date, project_id):
        self.event_no = event_no
        self.description = description
        self.supporint_documents = supporint_documents
        self.start_date = start_date
        self.end_date = end_date
        self.project_id = project_id
