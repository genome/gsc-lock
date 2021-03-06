from flask.ext.restful import fields
import simplejson


__all__ = [
    'claim_fields',
    'status_history_fields',
]


class Timedelta(fields.Raw):
    def format(self, value):
        return value.total_seconds()


class JSONEncoded(fields.Raw):
    def format(self, value):
        return simplejson.loads(value)


status_history_fields = {
    'status': fields.String,
    'timestamp': fields.DateTime,
}

claim_fields = {
    'url': fields.Url('claim', absolute=True),
    'active_duration': Timedelta,
    'created': fields.DateTime,
    'resource': fields.String,
    'status': fields.String,
    'status_history': fields.Nested(status_history_fields),
    'ttl': Timedelta,
    'user_data': JSONEncoded,
    'waiting_duration': Timedelta,
}
