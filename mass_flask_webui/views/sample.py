from flask import render_template, jsonify, flash, redirect, url_for
from mongoengine import DoesNotExist

from mass_flask_core.models import Sample, Report
from mass_flask_core.utils import PaginationFunctions, GraphFunctions
from mass_flask_webui.config import webui_blueprint


@PaginationFunctions.paginate
def _get_samples_paginated():
    return Sample.objects.get_with_tlp_level_filter()


@webui_blueprint.route('/sample/')
def sample_list():
    samples = _get_samples_paginated()
    return render_template('sample_list.html', samples=samples)


@webui_blueprint.route('/sample/<sample_id>/')
def sample_detail(sample_id):
    try:
        sample = Sample.objects.get_with_tlp_level_filter().get(id=sample_id)
        reports = Report.objects(sample=sample)
        return render_template('sample_detail.html', sample=sample, reports=reports)
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
