from flask.ext.restful import reqparse
import simplejson


__all__ = []


def pass_through_type(value):
    return value


_claim_post = reqparse.RequestParser()
_claim_post.add_argument('resource', type=str)
_claim_post.add_argument('ttl', type=float)
_claim_post.add_argument('user_data', type=pass_through_type)
def get_claim_post_data():
    data = _claim_post.parse_args()

    errors = {}

    if data['resource'] is None or data['resource'] == '':
        errors['resource'] = 'No resource specified'
    if data['ttl'] is None:
        errors['ttl'] = 'No ttl specified'
    elif data['ttl'] < 0:
        errors['ttl'] = 'Positive ttl required (in seconds)'

    data['user_data'] = simplejson.dumps(data['user_data'])

    return data, errors


_VALID_UPDATE_STATUSES = [
    'aborted',
    'active',
    'released',
    'revoked',
    'withdrawn',
]

_claim_update = reqparse.RequestParser()
_claim_update.add_argument('ttl', type=float)
_claim_update.add_argument('status', type=str)
def get_claim_update_data():
    data = _claim_update.parse_args()

    errors = {}

    if data['status'] is not None:
        if data['status'] not in _VALID_UPDATE_STATUSES:
            errors['status'] = 'Invalid value for status'
        if data['ttl'] is not None:
            errors['extra-parameters'] =\
                    'Only one parameter may be updated per request'

    if data['ttl'] is not None and data['ttl'] < 0:
        errors['ttl'] = 'Positive ttl required (in seconds)'

    if all(v is None for v in data.itervalues()):
        errors['missing-parameters'] = 'No parameters specified'

    return data, errors


_claim_list = reqparse.RequestParser()
_claim_list.add_argument('limit', type=int, location='args', default=10)
_claim_list.add_argument('offset', type=int, location='args', default=0)
_claim_list.add_argument('resource', type=str, location='args')
_claim_list.add_argument('status', type=str, location='args')
_claim_list.add_argument('minimum_active_duration', type=float, location='args')
_claim_list.add_argument('maximum_active_duration', type=float, location='args')
_claim_list.add_argument('minimum_waiting_duration', type=float,
        location='args')
_claim_list.add_argument('maximum_waiting_duration', type=float,
        location='args')
_claim_list.add_argument('minimum_ttl', type=float, location='args')
_claim_list.add_argument('maximum_ttl', type=float, location='args')
def get_claim_list_data():
    errors = {}
    try:
        data = _claim_list.parse_args()

    except:
        errors['message'] = 'Failed to parse query string'
        data = None

    return data, errors
