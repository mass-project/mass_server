from bson import DBRef
from flask import url_for, _request_ctx_stack, request
from marshmallow import ValidationError
from marshmallow_mongoengine import ModelSchema
import marshmallow.fields as mm_fields
from werkzeug.exceptions import NotFound


class SelfReferenceField(mm_fields.Field):
    def __init__(self, *args, **kwargs):
        endpoint = kwargs.pop('endpoint')
        super(SelfReferenceField, self).__init__(*args, **kwargs)
        self.dump_only = True
        self._endpoint = endpoint

    def serialize(self, attr, obj, accessor=None):
        return url_for(self._endpoint, id=obj.id, _external=True)


class ForeignReferenceField(mm_fields.Field):
    def __init__(self, endpoint, queryset, query_parameter='id', *args, **kwargs):
        super(ForeignReferenceField, self).__init__(*args, **kwargs)
        self._endpoint = endpoint
        self._queryset = queryset
        self._query_parameter = query_parameter

    def _serialize(self, value, attr, obj):
        if isinstance(value, DBRef):
            if self._query_parameter == 'id':
                query_parameter_value = value.id
            else:
                raise ValueError('Passed value is a DBRef and the query parameter is not the ObjectID!')
        else:
            query_parameter_value = value[self._query_parameter]
        kwargs = {
            'endpoint': self._endpoint,
            '_external': True,
            self._query_parameter: query_parameter_value,
        }
        return url_for(**kwargs)

    def _deserialize(self, value, attr=None, data=None):
        if not value.endswith('/'):
            value += '/'
        ctx = _request_ctx_stack.top
        adapter = ctx.url_adapter
        if adapter is None:
            raise RuntimeError('Could not find a URL adapter in the current request context.')

        local_url = value.replace(request.url_root, '/', 1)

        if local_url == value:
            raise ValidationError('Reference URL for field {} incorrectly specified: Network location of the URL does not match the servers network location.'.format(attr))

        try:
            endpoint, params = adapter.match(local_url, 'GET')
        except NotFound:
            raise ValidationError('Reference URL for field {} incorrectly specified: The path of the URL points to a nonexistent API endpoint.'.format(attr))

        blueprint_name = request.blueprint
        if self._endpoint[:1] == '.':
            if blueprint_name is not None:
                full_endpoint = blueprint_name + self._endpoint
            else:
                full_endpoint = self._endpoint[1:]
        else:
            full_endpoint = self._endpoint

        if endpoint != full_endpoint:
            print(endpoint)
            print(full_endpoint)
            raise ValidationError('Reference URL for field {} incorrectly specified. The path of the URL points to an endpoint that differs from the correct endpoint for this field.'.format(attr))

        query_result = self._queryset.filter(**params)

        if not query_result:
            raise ValidationError('Reference URL for field {} incorrectly specified. The format of the URL is correct but the referenced object could not be found.'.format(attr))

        return query_result.first()


class FileMapField(mm_fields.Field):
    def __init__(self, *args, **kwargs):
        endpoint = kwargs.pop('endpoint')
        file_url_key = kwargs.pop('file_url_key')
        super(FileMapField, self).__init__(*args, **kwargs)
        self.dump_only = True
        self._endpoint = endpoint
        self._file_url_key = file_url_key

    def _serialize(self, value, attr, obj):
        # return url_for(self._endpoint, id=obj.id, _external=True)
        result = {}
        for key in value.keys():
            kwargs = {
                'id': obj.id,
                self._file_url_key: key,
                '_external': True
            }
            result[key] = url_for(self._endpoint, **kwargs)
        return result

    def _deserialize(self, value, attr, data):
        raise ValidationError("Deserialization is not supported for this field.")


class BaseSchema(ModelSchema):
    class Meta:
        model_skip_values = []

