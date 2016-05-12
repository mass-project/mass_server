from flask import url_for, _request_ctx_stack, request
from marshmallow import ValidationError, post_dump, MarshalResult
from marshmallow_mongoengine import ModelSchema
from marshmallow_mongoengine.convert import default_converter
import marshmallow.fields as mm_fields
import marshmallow_mongoengine.fields as mmme_fields
from werkzeug.exceptions import NotFound


# Make these importable by other modules
mm_fields = mm_fields
mmme_fields = mmme_fields


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

    # def serialize(self, attr, obj, accessor=None):
    #     kwargs = {
    #         'endpoint': self._endpoint,
    #         '_external': True,
    #         self._query_parameter: obj[attr][self._query_parameter],
    #     }
    #     return url_for(**kwargs)

    def _serialize(self, value, attr, obj):
        kwargs = {
            'endpoint': self._endpoint,
            '_external': True,
            self._query_parameter: value[self._query_parameter],
        }
        return url_for(**kwargs)

    def deserialize(self, value, attr=None, data=None):
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

        if endpoint != self._endpoint:
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


class DynamicBaseSchema(BaseSchema):
    @staticmethod
    def _serialize_dynamic_fields(obj, serialized_data):
        if obj._dynamic:
            for name, field in obj._dynamic_fields.items():
                serialized_data[name] = default_converter.convert_field(field).serialize(name, obj)

    def dump(self, obj, many=None, update_fields=True, **kwargs):
        if self.many:
            data = []
            errors = []
            for item in obj:
                result = super(DynamicBaseSchema, self).dump(item, many=False, update_fields=update_fields, **kwargs)
                self._serialize_dynamic_fields(item, result.data)
                data.append(result.data)
                if result.errors:
                    errors.append(result.errors)
            return MarshalResult(data, errors)
        else:
            result = super(DynamicBaseSchema, self).dump(obj, many=False, update_fields=update_fields, **kwargs)
            self._serialize_dynamic_fields(obj, result.data)
            return result

    def load(self, data, many=None, partial=None, **kwargs):
        result = super(DynamicBaseSchema, self).load(data, many=many, partial=partial, **kwargs)
        if self.many:
            print('Fix me!')
        else:
            for key, value in data.items():
                if key not in result.data._fields:
                    setattr(result.data, key, value)
        return result

