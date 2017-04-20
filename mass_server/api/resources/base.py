from flask import jsonify, request
from flask.views import MethodView
from mongoengine import DoesNotExist
from datetime import datetime

from mass_server.core.utils import PaginationFunctions
from mass_server.api.schemas import SchemaMapping


class Ref(object):

    def __init__(self, key):
        self.key = key

    def resolve(self, obj):
        return getattr(obj, self.key, None)


class BaseResource(MethodView):
    schema = None
    pagination_schema = None
    model_class = None
    query_key_field = None
    filter_parameters = []

    @staticmethod
    def _create_date_from_string(string):
        return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S+00:00')

    @staticmethod
    def _create_list_from_string(string):
        return string.split(',')

    @property
    def schema(self):
        return Ref('schema').resolve(self)

    @property
    def pagination_schema(self):
        return Ref('pagination_schema').resolve(self)

    @property
    def model_class(self):
        return Ref('model_class').resolve(self)

    @property
    def query_key_field(self):
        return Ref('query_key_field').resolve(self)

    @property
    def filter_parameters(self):
        return Ref('filter_parameters').resolve(self)

    @PaginationFunctions.paginate
    def _get_list(self):
        filter_condition = {}
        for parameter, parameter_type in self.filter_parameters:
            if parameter in request.args:
                filter_condition[parameter] = parameter_type(request.args[parameter])

        return self.schema.Meta.model.objects.filter(**filter_condition)

    def get_list(self):
        paginated_objects = self._get_list()
        serialized_objects = []
        for obj in paginated_objects['results']:
            schema = SchemaMapping.get_schema_for_model_class(obj.__class__.__name__)
            serialized_objects.append(schema.dump(obj).data)
        return jsonify({
            'results': serialized_objects,
            'next': paginated_objects['next'],
            'previous': paginated_objects['previous']
        })

    def get_detail(self, **kwargs):
        query_filter = {
            self.query_key_field: kwargs[self.query_key_field]
        }
        try:
            obj = self.schema.Meta.model.objects.get(**query_filter)
            print(obj)
            schema = SchemaMapping.get_schema_for_model_class(obj.__class__.__name__)
            result = schema.dump(obj)
            return jsonify(result.data)
        except DoesNotExist:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404

    def get(self, **kwargs):
        if self.query_key_field not in kwargs or kwargs[self.query_key_field] is None:
            return self.get_list()
        else:
            return self.get_detail(**kwargs)

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        else:
            parsed_data = self.schema.load(json_data, partial=True)
            if parsed_data.errors:
                return jsonify(parsed_data.errors), 400
            obj = parsed_data.data
            obj.save()
            result = self.schema.dump(obj)
            return jsonify(result.data), 201

    def put(self, **kwargs):
        json_data = request.get_json()
        if kwargs[self.query_key_field] is None:
            return jsonify({'error': 'Parameter \'{}\' must be specified'.format(self.query_key_field)}), 400
        elif not json_data:
            return jsonify({'error': 'No JSON data provided. Make sure to set the content type of your request to: application/json'}), 400
        else:
            query_filter = {
                self.query_key_field: kwargs[self.query_key_field]
            }
            try:
                obj = self.schema.model.objects.get(**query_filter)
                obj.modify(**json_data)
                result = self.schema.dump(obj)
                return jsonify(result.data)
            except DoesNotExist:
                return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404

    def delete(self, **kwargs):
        if kwargs[self.query_key_field] is None:
            return jsonify({'error': 'Parameter \'{}\' must be specified'.format(self.query_key_field)}), 400
        else:
            query_filter = {
                self.query_key_field: kwargs[self.query_key_field]
            }
            try:
                obj = self.schema.model.objects.get(**query_filter)
                obj.delete()
                return '', 204
            except DoesNotExist:
                return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404
