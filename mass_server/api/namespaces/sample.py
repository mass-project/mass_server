import json

from flask import request
from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, load_json, catch, paginate, filter_results
from mongoengine import ValidationError

from mass_server.api.config import api

from mass_server.api.schemas import ReportSchema, SampleSchema, SampleRelationSchema
from mass_server.api.utils import pagination_helper, MappedQuerysetFilter
from mass_server.core.models import Report, Sample, SampleRelation
from mass_server.core.utils import GraphFunctions
from mass_server.queue.queue_context import channel, ensure_connection


@api.add_namespace('/sample')
class SampleNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(SampleSchema(), paginated=True)
    @paginate(pagination_helper)
    @filter_results(MappedQuerysetFilter(Sample.filter_parameters), Sample.filter_parameters.keys())
    def collection_get(self):
        return Sample.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(SampleSchema(), return_code=201)
    @catch(ValueError, 'The request body is malformed or incomplete.', error_code=400)
    @catch(ValidationError, 'The request body is malformed or incomplete.', error_code=400)
    def collection_post(self):
        json_data = request.get_json()
        ensure_connection()
        if json_data:
            channel.basic_publish(exchange='', routing_key='es_samples', body={"data": json_data})
            return Sample.create_or_update(**json_data)
        else:
            if 'metadata' in request.form:
                json_data = json.loads(request.form['metadata'])
                channel.basic_publish(exchange='', routing_key='es_samples', body={"data": json_data})
            else:
                json_data = {}
            if 'file' in request.files:
                if not 'unique_features' in json_data:
                    json_data['unique_features'] = {}
                json_data['unique_features']['file'] = request.files['file']
            return Sample.create_or_update(**json_data)

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/')
    @catch(Sample.DoesNotExist, 'No sample with the specified id found.', 404)
    @dump(SampleSchema())
    def element_get(self, id):
        return Sample.objects.get(id=id)

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/', methods=['PATCH'])
    @catch(Sample.DoesNotExist, 'No sample with the specified id found.', 404)
    @dump(SampleSchema())
    @catch(ValueError, 'The request body is malformed or incomplete.', error_code=400)
    @catch(ValidationError, 'The request body is malformed or incomplete.', error_code=400)
    def element_patch(self, id):
        sample = Sample.objects.get(id=id)
        json_data = request.get_json()
        if json_data:
            sample.update(**json_data)
            sample.save()
            return sample

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/delivery_dates/')
    @catch(Sample.DoesNotExist, 'No sample with the specified id found.', 404)
    def delivery_dates(self, id):
        delivery_dates = Sample.objects.get(id=id).delivery_dates
        return json.dumps([date.isoformat() for date in delivery_dates]), 200

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/download/')
    @catch(Sample.DoesNotExist, 'No sample with the specified id found.', 404)
    @catch(ValueError, 'This sample contains no file.', 400)
    def download(self, id):
        sample = Sample.objects.get(id=id)
        if not sample.unique_features.file:
            raise ValueError('Sample has no file.')
        return sample.unique_features.file.file.read(), 200, {'Content-Type': 'application/octet-stream'}

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/relation_graph/')
    @catch(Sample.DoesNotExist, 'No sample with the specified id found.', 404)
    @dump(SampleRelationSchema(), paginated=True)
    @paginate(pagination_helper)
    def relation_graph(self, id):
        sample = Sample.objects.get(id=id)
        if 'depth' in request.args:
            sample_relations = GraphFunctions.get_relation_graph(sample, int(request.args['depth']))
        else:
            sample_relations = GraphFunctions.get_relation_graph(sample)

        relation_ids = [x.id for x in sample_relations]
        return SampleRelation.objects(id__in=relation_ids).no_dereference()

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/<id>/reports/')
    @catch(Sample.DoesNotExist, 'No sample with the specified id found.', 404)
    @dump(ReportSchema(), paginated=True)
    @paginate(pagination_helper)
    def reports(self, id):
        sample = Sample.objects.get(id=id)
        return Report.objects(sample=sample)
