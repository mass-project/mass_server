import json

from flask import request
from flask_modular_auth import privilege_required, AuthenticatedPrivilege, RolePrivilege
from flask_slimrest.decorators import add_endpoint, dump, load, load_json, catch, paginate
from flask_slimrest.utils import make_api_error_response
from mongoengine import ValidationError

from mass_server.api.config import api
from mass_server.api.schemas import SampleSchema, SampleRelationSchema
from mass_server.api.utils import pagination_helper
from mass_server.core.models import Sample, SampleRelation
from mass_server.core.utils import GraphFunctions


@api.add_namespace('/sample')
class SampleNamespace:
    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/')
    @dump(SampleSchema(), paginated=True)
    @paginate(pagination_helper)
    def collection_get(self):
        return Sample.objects

    @privilege_required(AuthenticatedPrivilege())
    @add_endpoint('/', methods=['POST'])
    @dump(SampleSchema(), return_code=201)
    @catch(ValueError, 'The request body is malformed or incomplete.', error_code=400)
    @catch(ValidationError, 'The request body is malformed or incomplete.', error_code=400)
    def collection_post(self):
        json_data = request.get_json()
        if json_data:
            return Sample.create_or_update(**json_data)
        else:
            if 'metadata' in request.form:
                json_data = json.loads(request.form['metadata'])
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
        return sample_relations
