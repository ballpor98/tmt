import json
from typing import Callable


def get_authorized_header(query_fn: Callable, username: str, password: str) -> dict:
    query_str = (
        '''
        mutation getToken($username: String!, $password: String!){
            obtainToken(username: $username, password: $password){
            token
            payload
            refreshExpiresIn
          }
        }
        '''
    )
    variables = {
        'username': username,
        'password': password,
    }
    response = query_fn(query=query_str, variables=variables)
    content = json.loads(response.content)
    token = content['data']['obtainToken']['token']
    return {'HTTP_AUTHORIZATION': f'Bearer {token}'}
