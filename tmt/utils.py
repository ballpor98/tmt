from datetime import datetime
from graphql_jwt.settings import jwt_settings

from tmt.clocking.models import User


def jwt_payload(user: User, context=None):
    jwt_datetime = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA
    jwt_expires = int(jwt_datetime.timestamp())
    payload = {
        'username': str(user.username),
        'sub': str(user.id),
        'sub_name': user.username,
        'sub_email': user.email,
        'exp': jwt_expires,
    }
    return payload


def check_auth(user: User):
    if user.is_anonymous:
        raise Exception('Authentication Failure: Your must be signed in')
