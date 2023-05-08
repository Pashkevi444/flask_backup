# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AIS.us
"""
import os
from apps.projects import blueprint
from apps import db
from flask import render_template, redirect, request, url_for, abort, jsonify
from flask_login import login_required
from apps.projects.forms import ProjectForm, ProjectDetailForm, ProjectProgressForm, ProjectEventForm
from apps.projects.models import Projects, ProjectsDetails, ProjectsProgress, ProjectsDelayEvents
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pathlib import Path
from apps.projects.view import projectsController
from datetime import datetime, date

@blueprint.route('/projects')
def index():
    projects = Projects.query.all()
    return render_template('/projects/index.html', projects=projects)


@blueprint.route('/projects/<int:project_id>', methods=['GET'])
def project_detail(project_id):
    total = 4
    projects = Projects.query.all()
    project = Projects.query.get(project_id)
    project_details = ProjectsDetails.query.filter_by(project_id=project_id).all()
    return render_template('/projects/detail_ag.html', projects=projects, project=project, project_details=project_details)


@blueprint.route('/api/project/<int:project_id>')
def data(project_id):
    details_list = []
    project_details = ProjectsDetails.query.filter_by(project_id=project_id).all()
    for row in project_details:
        formatted_row = {'id': row.id, 'phase': row.phase, 'ld_rate_per_delay': row.ld_rate_per_delay, 'description': row.description}
        join_date_str = row.loa_start_date.strftime('%Y-%m-%d')
        join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
        formatted_row['loa_start_date'] = join_date.strftime('%d/%m/%Y')
        loa_completion_date_str = row.loa_completion_date.strftime('%Y-%m-%d')
        loa_completion_date = datetime.strptime(loa_completion_date_str, '%Y-%m-%d')
        formatted_row['loa_completion_date'] = loa_completion_date.strftime('%d/%m/%Y')
        details_list.append(formatted_row)
    # response
    return jsonify(details_list)



@blueprint.route('/api/update', methods=['POST'])
def update():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    if data['entity'] == 'details':
        user = ProjectsDetails.query.get(data['id'])
        for field in ['phase', 'description', 'loa_start_date', 'loa_completion_date', 'ld_rate_per_delay']:
            if field in data:
                setattr(user, field, data[field])
        db.session.commit()
        return '', 204
    if data['entity'] == 'progress':
        user = ProjectsProgress.query.get(data['id'])
        for field in ['phase', 'description', 'ss_start_date_1', 'ss_completion_date_1', 'ss_start_date_2',
                      'ss_completion_date_2']:
            if field in data:
                if field in ['ss_start_date_1', 'ss_completion_date_1', 'ss_start_date_2', 'ss_completion_date_2']:
                    try:
                        # Attempt to parse the date value from the input data
                        date_val = datetime.strptime(data[field], '%d/%m/%Y').date()
                    except (ValueError, TypeError):
                        # If the value cannot be parsed as a date, set the date value to None
                        date_val = None
                    setattr(user, field, date_val)
                else:
                    setattr(user, field, data[field])
        db.session.commit()
        return jsonify({'success': True})
    if data['entity'] == 'event':
        user = ProjectsDelayEvents.query.get(data['id'])
        for field in ['event_no', 'description', 'supporint_documents', 'start_date', 'end_date']:
            if field in data:
                setattr(user, field, data[field])
        db.session.commit()
        return '', 204

@blueprint.route('/api/delete', methods=['POST'])
def delete():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    if data['entity'] == 'event':
        record = ProjectsDelayEvents.query.get(data['id'])
        if record:
            db.session.delete(record)
            db.session.commit()
        db.session.commit()
        return '', 204
    if data['entity'] == 'detail':
        record = ProjectsDetails.query.get(data['id'])
        if record:
            db.session.delete(record)
            db.session.commit()
        db.session.commit()
        return '', 204
    if data['entity'] == 'progress':
        record = ProjectsProgress.query.get(data['id'])
        if record:
            db.session.delete(record)
            db.session.commit()
        db.session.commit()
        return '', 204


@blueprint.route('/api/project_progress/<int:project_id>')
def data_progress(project_id):
    progress_list = []
    project_progress = ProjectsProgress.query.filter_by(project_id=project_id).all()
    for row in project_progress:
        formatted_row = {'id': row.id, 'phase': row.phase, 'description': row.description}
        join_date_str = row.ss_start_date_1.strftime('%Y-%m-%d')
        join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
        formatted_row['ss_start_date_1'] = join_date.strftime('%d/%m/%Y')
        formatted_row['ss_completion_date_1'] = row.ss_completion_date_1
        formatted_row['ss_start_date_2'] = row.ss_start_date_2
        formatted_row['ss_completion_date_2'] = row.ss_completion_date_2
        progress_list.append(formatted_row)
    # response
    return jsonify(progress_list)


@blueprint.route('/api/project_progress', methods=['POST'])
def update_progress():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    user = ProjectsDetails.query.get(data['id'])
    for field in ['name', 'age', 'address', 'phone', 'email']:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return '', 204


@blueprint.route('/api/project_event/<int:project_id>')
def data_event(project_id):
    project_events = ProjectsDelayEvents.query.filter_by(project_id=project_id).all()
    events_list = [{'id': detail.id, 'event_no': detail.event_no,
                    'description': detail.description,
                    'supporint_documents': detail.supporint_documents,
                    'start_date': detail.start_date,
                    'end_date': detail.end_date} for detail in project_events]
    total = 4

    # response
    return {
        'data': events_list,
        'total': total,
    }


@blueprint.route('/api/project_event', methods=['POST'])
def update_event():
    data = request.get_json()
    if 'id' not in data:
        abort(400)
    user = ProjectsDetails.query.get(data['id'])
    for field in ['name', 'age', 'address', 'phone', 'email']:
        if field in data:
            setattr(user, field, data[field])
    db.session.commit()
    return '', 204





@blueprint.route('/projects/<int:project_id>/add_detail', methods=['GET'])
def add_project_detail_item_form(project_id):
    project = Projects.query.get(project_id)
    create_project_form = ProjectDetailForm(request.form)
    return render_template('/projects/add_detail.html', form=create_project_form, project=project)


@blueprint.route('/projects/<int:project_id>/add_progress', methods=['GET'])
def add_project_progress_item_form(project_id):
    project = Projects.query.get(project_id)
    create_project_form = ProjectProgressForm(request.form)
    return render_template('/projects/add_progress.html', form=create_project_form, project=project)


@blueprint.route('/projects/<int:project_id>/add_event', methods=['GET'])
def add_project_event_item_form(project_id):
    project = Projects.query.get(project_id)
    create_project_form = ProjectEventForm(request.form)
    return render_template('/projects/add_event.html', form=create_project_form, project=project)

@blueprint.route('/projects/add', methods=['GET'])
def add_project_item_form():
    create_project_form = ProjectForm(request.form)
    return render_template('/projects/add.html', form=create_project_form)

# Add a route to handle the form submission
@blueprint.route('/projects/add', methods=['POST'])
def add_project_item():
    create_project_form = ProjectForm()
    name = create_project_form.name.data
    number = create_project_form.number.data
    value = create_project_form.value.data
    picture = create_project_form.picture.data
    if isinstance(picture, FileStorage):
        # If picture is a FileStorage object, process it as usual
        filename = secure_filename(picture.filename)
        filepath = os.path.join('apps/static/uploads', filename)
        picture.save(filepath)
    elif isinstance(picture, str):
        # If picture is a string, it represents a file path
        filename = Path(picture).name
        # Perform any necessary processing or file copying here

    # Save the form data to the database
    project = Projects(name=name, value=value, number=number, preview_picture=filename)
    db.session.add(project)
    db.session.commit()

    return redirect('/projects')







# Add a route to handle the form submission
@blueprint.route('/projects/<int:project_id>/add_detail', methods=['POST'])
def add_project_detail_item(project_id):
    phaseCountForProject = projectsController.getMaxPhase(project_id, ProjectsDetails)
    increasedPhaseCountForProject = phaseCountForProject+1
    project = Projects.query.get(project_id)
    create_project_form = ProjectDetailForm()
    description = create_project_form.description.data
    loa_start_date = create_project_form.loa_start_date.data
    loa_completion_date = create_project_form.loa_completion_date.data
    ld_rate_per_delay = create_project_form.ld_rate_per_delay.data

    # Save the form data to the database
    project_detail_info = ProjectsDetails(phase=increasedPhaseCountForProject,
                                          description=description,
                                          loa_start_date=loa_start_date,
                                          loa_completion_date=loa_completion_date,
                                          ld_rate_per_delay=ld_rate_per_delay,
                                          project_id=project_id)
    db.session.add(project_detail_info)
    db.session.commit()
    new_url = f'/projects/{project_id}'
    return redirect(new_url)


@blueprint.route('/projects/<int:project_id>/add_progress', methods=['POST'])
def add_project_progress_item(project_id):
    create_project_form = ProjectProgressForm()
    phaseCountForProject = projectsController.getMaxPhase(project_id, ProjectsProgress)
    increasedPhaseCountForProject = phaseCountForProject + 1
    description = create_project_form.description.data
    ss_start_date_1 = create_project_form.ss_start_date_1.data
    ss_completion_date_1 = create_project_form.ss_completion_date_1.data
    ss_start_date_2 = create_project_form.ss_start_date_2.data
    ss_completion_date_2 = create_project_form.ss_completion_date_2.data
    # Save the form data to the database
    project_detail_info = ProjectsProgress(phase=increasedPhaseCountForProject,
                                           description=description,
                                           ss_start_date_1=ss_start_date_1,
                                           ss_completion_date_1=ss_completion_date_1,
                                           ss_start_date_2=ss_start_date_2,
                                           ss_completion_date_2=ss_completion_date_2,
                                           project_id=project_id)
    db.session.add(project_detail_info)
    db.session.commit()

    new_url = f'/projects/{project_id}'
    return redirect(new_url)


@blueprint.route('/projects/<int:project_id>/add_event', methods=['POST'])
def add_project_event_item(project_id):
    create_project_form = ProjectEventForm()
    event_no = create_project_form.event_no.data
    description = create_project_form.description.data
    supporint_documents = create_project_form.supporint_documents.data
    start_date = create_project_form.start_date.data
    end_date = create_project_form.end_date.data

    # Save the form data to the database
    project_detail_info = ProjectsDelayEvents(event_no=event_no,
                                              description=description,
                                              supporint_documents=supporint_documents,
                                              start_date=start_date,
                                              end_date=end_date, project_id=project_id)
    db.session.add(project_detail_info)
    db.session.commit()

    new_url = f'/projects/{project_id}'
    return redirect(new_url)
