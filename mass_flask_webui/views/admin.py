import inspect

from flask import current_app, render_template, request, flash
from flask.ext.login import current_user
from functools import wraps

from mass_flask_config.app import db
from mass_flask_core import models
from mass_flask_core.models import AnalysisSystem, AnalysisSystemInstance, InstanceAPIKey
from mass_flask_webui.config import webui_blueprint


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_admin:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view


def _get_db_statistics():
    result = []
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and issubclass(obj, db.Document):
            result.append((name, obj.objects.count()))
    return result


@webui_blueprint.route('/admin/', methods=['GET'])
@admin_required
def admin():
    _get_db_statistics()
    return render_template('admin/admin.html', database_statistics=_get_db_statistics())


@webui_blueprint.route('/admin/analysis_systems/', methods=['GET', 'POST'])
@admin_required
def admin_analysis_systems():
    if request.method == 'POST':
        _process_analysis_system_action()
    analysis_systems = AnalysisSystem.objects()
    for system in analysis_systems:
        system.instances = AnalysisSystemInstance.objects(analysis_system=system.id)
        for instance in system.instances:
            instance.api_key = InstanceAPIKey.get_or_create(instance).generate_auth_token()
    return render_template('admin/analysis_systems.html', analysis_systems=analysis_systems)


def _process_analysis_system_action():
    action = request.form['action']
    if action == 'delete_instance':
        _delete_instance()
    elif action == 'create_instance':
        _create_instance()
    elif action == 'regenerate_api_key':
        _regenerate_api_key()
    else:
        flash('Unknown operation requested.', 'danger')


def _delete_instance():
    instance = AnalysisSystemInstance.objects(uuid=request.form['uuid']).first()
    if instance:
        instance.delete()
        flash('Analysis system instance deleted!', 'success')
    else:
        flash('Delete failed - UUID not found!', 'danger')


def _create_instance():
    analysis_system = AnalysisSystem.objects(id=request.form['analysis_system']).first()
    if analysis_system:
        if request.form['uuid']:
            instance = AnalysisSystemInstance(analysis_system=analysis_system, uuid=request.form['uuid'])
        else:
            instance = AnalysisSystemInstance(analysis_system=analysis_system)
        instance.save()
        flash('Analysis system instance created!', 'success')
    else:
        flash('Cannot create analysis system instance - System not found!', 'danger')


def _regenerate_api_key():
    instance = AnalysisSystemInstance.objects(uuid=request.form['uuid']).first()
    key = InstanceAPIKey.objects(instance=instance.id).first()
    if key:
        key.delete()
        flash('Old API key deleted! New key will be automatically generated.', 'success')
    else:
        flash('Could not find the old API key associated to this instance UUID!', 'danger')