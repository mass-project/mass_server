from flask import render_template, jsonify, flash, redirect, url_for
from mongoengine import DoesNotExist

from flask_modular_auth import current_authenticated_entity
from mass_flask_core.models import Sample, Report, ScheduledAnalysis, AnalysisSystem, AnalysisRequest
from mass_flask_core.utils import PaginationFunctions, GraphFunctions, TimeFunctions
from mass_flask_webui.config import webui_blueprint
from mass_flask_webui.forms.comment import CommentForm
from mass_flask_webui.forms.request_analysis import RequestAnalysisForm


@PaginationFunctions.paginate
def _get_samples_paginated():
    return Sample.objects.get_with_tlp_level_filter()


@webui_blueprint.route('/sample/')
def sample_list():
    samples = _get_samples_paginated()
    return render_template('sample_list.html', samples=samples)


@webui_blueprint.route('/sample/<sample_id>/', methods=['GET', 'POST'])
def sample_detail(sample_id):
    try:
        sample = Sample.objects.get_with_tlp_level_filter().get(id=sample_id)
        comment_form = CommentForm()
        if comment_form.validate_on_submit():
            sample.add_comment(comment_form.data['comment'], TimeFunctions.get_timestamp(), current_authenticated_entity._get_current_object())
            sample.save()
            flash('Your comment has been added', 'success')
            return redirect(url_for('.sample_detail', sample_id=sample.id))
        reports = Report.objects(sample=sample)

        analysis_systems = []
        for system in AnalysisSystem.objects:
            analysis_systems.append((system.identifier_name, system.verbose_name))

        request_form = RequestAnalysisForm()
        request_form.analysis_system.choices = analysis_systems

        if request_form.validate_on_submit():
            priority = request_form.data['priority']
            analysis_system = AnalysisSystem.objects.get(identifier_name=request_form.data['analysis_system'])
            try:
                request = AnalysisRequest.objects.get(sample=sample, analysis_system=analysis_system)
                request.priority = priority
            except DoesNotExist:
                request = AnalysisRequest(sample=sample, analysis_system=analysis_system, priority=priority)
            request.save()

        requested_analyses = AnalysisRequest.objects(sample=sample)

        activity = [{
            'class': 'info',
            'glyph': 'fa-paper-plane',
            'title': 'Sample delivered to MASS',
            'timestamp': sample.delivery_date
        },
        {
            'class': 'info',
            'glyph': 'fa-star',
            'title': 'First known occurrence of the sample',
            'timestamp': sample.first_seen
        }
        ]
        for report in reports:
            activity.append({
                'class': 'success',
                'glyph': 'fa-search',
                'title': '{} report added'.format(report.analysis_system.verbose_name),
                'timestamp': report.upload_date
            })
        for comment in sample.comments:
            activity.append({
                'class': '',
                'glyph': 'fa-comment',
                'title': '{} added a comment'.format(comment.user.username),
                'timestamp': comment.post_date,
                'content': comment.comment
            })
        sorted_activity = sorted(activity, key=lambda k: k['timestamp'])

        return render_template('sample_detail.html', sample=sample, reports=reports, activity=sorted_activity,
                               comment_form=comment_form, requested_analyses=requested_analyses,
                               analysis_systems=analysis_systems, schedule_form=request_form)
    except DoesNotExist:
        flash('Sample not found or you do not have access to this sample.', 'warning')
        return redirect(url_for('.index'))


@webui_blueprint.route('/sample/<sample_id>/graph/')
def sample_graph(sample_id):
    try:
        sample = Sample.objects.get_with_tlp_level_filter().get(id=sample_id)
        relations = GraphFunctions.get_relation_graph(sample)
        node_ids = set()
        node_ids.add(sample.id)
        edges = []
        for edge in relations:
            edges.append({
                'source': str(edge.sample.id),
                'target': str(edge.other.id)
            })
            node_ids.add(edge.sample.id)
            node_ids.add(edge.other.id)
        samples = Sample.objects.get_with_tlp_level_filter().filter(id__in=node_ids)
        nodes = []
        for node in samples:
            nodes.append({
                'id': str(node.id),
                'label': node.title
            })
        response = jsonify({'edges': edges, 'nodes': nodes})
        return response, 200, {'Content-Type': 'application/json'}
    except DoesNotExist:
        return jsonify({'error': 'Sample not found or you do not have access to this sample.'}), 404, {'Content-Type': 'application/json'}
