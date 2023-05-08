# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AIS.us
"""

from apps.catalog import blueprint
from apps import db
from flask import render_template, redirect, request, url_for
from flask_login import login_required
from apps.catalog.forms import CatalogForm
from apps.catalog.models import Catalog



@blueprint.route('/catalog')

def index():
    projects = Catalog.query.all()
    return render_template('/catalog/index.html', todos=projects)


@blueprint.route('/add', methods=['POST'])
def add():
    form = CatalogForm()
    title = form.title.data
    new_catalog = Catalog(title)
    db.session.add(new_catalog)
    db.session.commit()
    return redirect('/')


@blueprint.route('/update/<int:id>', methods=['POST'])
def update(id):
    catalog = Catalog.query.get(id)
    catalog.completed = not catalog.completed
    db.session.commit()
    return redirect('/')

@blueprint.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    catalog = Catalog.query.get(id)
    db.session.delete(catalog)
    db.session.commit()
    return redirect('/')