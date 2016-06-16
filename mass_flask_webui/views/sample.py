from flask import render_template, jsonify, Response

from mass_flask_core.models import Sample, Report
from mass_flask_core.utils import PaginationFunctions, GraphFunctions
from mass_flask_webui.config import webui_blueprint


@PaginationFunctions.paginate(per_page=100)
def _get_samples_paginated():
    return Sample.objects()


@webui_blueprint.route('/sample/')
def sample_list():
    samples = _get_samples_paginated()
    return render_template('sample_list.html', samples=samples)


@webui_blueprint.route('/sample/<sample_id>/')
def sample_detail(sample_id):
    sample = Sample.objects(id=sample_id).first()
    reports = Report.objects(sample=sample)
    return render_template('sample_detail.html', sample=sample, reports=reports)


@webui_blueprint.route('/sample/<sample_id>/graph/')
def sample_graph(sample_id):
    sample = Sample.objects(id=sample_id).first()
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
    samples = Sample.objects(id__in=node_ids)
    nodes = []
    for node in samples:
        nodes.append({
            'id': str(node.id),
            'label': node.title
        })
    response = jsonify({'edges': edges, 'nodes': nodes})
    return response, 200, {'Content-Type': 'application/json'}
