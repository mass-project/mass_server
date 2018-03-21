from flask import render_template, jsonify, flash, redirect, url_for
from flask_modular_auth import current_authenticated_entity
from mongoengine import DoesNotExist

from mass_server.webui.config import webui_blueprint
from mass_server.core.utils import PaginationFunctions, GraphFunctions, TimeFunctions
from mass_server.core.models import Sample, Report, ScheduledAnalysis, AnalysisSystem, AnalysisRequest
from mass_server.webui.forms import CommentForm, RequestAnalysisForm


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
        _process_comment_form(comment_form, sample)
        request_form = RequestAnalysisForm()
        _process_request_form(request_form, sample)

        requested_analyses = AnalysisRequest.objects(sample=sample)
        scheduled_analyses = ScheduledAnalysis.objects(sample=sample)

        reports = Report.objects(sample=sample)
        activity = [{
            'class': 'info',
            'glyph': 'fa-star',
            'title': 'First known occurrence of the sample',
            'timestamp': sample.first_seen
        }]
        for date in sample.delivery_dates:
            activity.append({
                'class': 'info',
                'glyph': 'fa-paper-plane',
                'title': 'Sample delivered to MASS',
                'timestamp': date
            })
        for report in reports:
            activity.append({
                'class':
                'success',
                'glyph':
                'fa-search',
                'title':
                '{} report added'.format(report.analysis_system.verbose_name),
                'timestamp':
                report.upload_date
            })
        for comment in sample.comments:
            activity.append({
                'class':
                '',
                'glyph':
                'fa-comment',
                'title':
                '{} added a comment'.format(comment.user.username),
                'timestamp':
                comment.post_date,
                'content':
                comment.comment
            })
        sorted_activity = sorted(activity, key=lambda k: k['timestamp'])

        return render_template(
            'sample_detail.html',
            sample=sample,
            reports=reports,
            activity=sorted_activity,
            comment_form=comment_form,
            requested_analyses=requested_analyses,
            scheduled_analyses=scheduled_analyses,
            request_form=request_form)
    except DoesNotExist:
        flash('Sample not found or you do not have access to this sample.',
              'warning')
        return redirect(url_for('.index'))


def _process_comment_form(form, sample):
    if form.validate_on_submit():
        sample.add_comment(form.data['comment'],
                           TimeFunctions.get_timestamp(),
                           current_authenticated_entity._get_current_object())
        sample.save()
        flash('Your comment has been added', 'success')
        return redirect(url_for('.sample_detail', sample_id=sample.id))


def _process_request_form(form, sample):
    if form.validate_on_submit(
    ) and current_authenticated_entity.is_authenticated:
        priority = form.data['priority']
        analysis_system = AnalysisSystem.objects.get(
            identifier_name=form.data['analysis_system'])
        request = AnalysisRequest(
            sample=sample,
            analysis_system=analysis_system,
            schedule_after=form.data['schedule_after'],
            priority=priority)

        request.save()
        flash('Your request has been saved', 'success')


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
        samples = Sample.objects.get_with_tlp_level_filter().filter(
            id__in=node_ids)
        nodes = []
        for node in samples:
            nodes.append({'id': str(node.id), 'label': node.title})
        response = jsonify({'edges': edges, 'nodes': nodes})
        return response, 200, {'Content-Type': 'application/json'}
    except DoesNotExist:
        return jsonify({
            'error':
            'Sample not found or you do not have access to this sample.'
        }), 404, {
            'Content-Type': 'application/json'
        }
