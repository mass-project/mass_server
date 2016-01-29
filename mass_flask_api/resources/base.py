from flask import jsonify, request
from flask.views import MethodView
from mass_flask_api.utils import paginate


class Ref(object):

    def __init__(self, key):
        self.key = key

    def resolve(self, obj):
        return getattr(obj, self.key, None)


class BaseResource(MethodView):
    schema = None
    pagination_schema = None
    model = None
    query_key_field = None

    @property
    def schema(self):
        return Ref('schema').resolve(self)

    @property
    def pagination_schema(self):
        return Ref('pagination_schema').resolve(self)

    @property
    def model(self):
        return Ref('model').resolve(self)

    @property
    def query_key_field(self):
        return Ref('query_key_field').resolve(self)

    @paginate
    def _get_list(self):
        return self.model.objects

    def get_list(self):
        paginated_objects = self._get_list()
        result = self.pagination_schema.dump(paginated_objects)
        return jsonify(result.data)

    def get_detail(self, **kwargs):
        query_filter = {
            self.query_key_field: kwargs[self.query_key_field]
        }
        obj = self.model.objects(**query_filter).first()
        if not obj:
            return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404
        else:
            result = self.schema.dump(obj)
            return jsonify(result.data)

    def get(self, **kwargs):
        if kwargs[self.query_key_field] is None:
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
            obj = self.model.objects(**query_filter).first()
            if not obj:
                return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404
            else:
                obj.modify(**json_data)
                result = self.schema.dump(obj)
                return jsonify(result.data)

    def delete(self, **kwargs):
        if kwargs[self.query_key_field] is None:
            return jsonify({'error': 'Parameter \'{}\' must be specified'.format(self.query_key_field)}), 400
        else:
            query_filter = {
                self.query_key_field: kwargs[self.query_key_field]
            }
            obj = self.model.objects(**query_filter).first()
            if not obj:
                return jsonify({'error': 'No object with key \'{}\' found'.format(kwargs[self.query_key_field])}), 404
            else:
                obj.delete()
                return '', 204
