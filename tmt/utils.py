from datetime import datetime
from graphql_jwt.settings import jwt_settings


def jwt_payload(user, context=None):
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
