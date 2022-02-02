import json

from graphene_django.utils.testing import GraphQLTestCase

from tests.utils import get_authorized_header
from tmt.clocking.models import User

GraphQLTestCase.GRAPHQL_URL = '/graphql'

clock_in_query_str = (
    '''
    mutation clockIn{
        clockIn{
            clock{
                id
                user{
                    id
                    username
                    email
                }
                clockedIn
                clockedOut
            }
        }
    }
    '''
)


class ClockInTestCase(GraphQLTestCase):
    def setUp(self):
        username = 'janedoe'
        email = 'j.doe@test'
        password = 'top_secret'
        self.user = User.objects.create_user(
            username=username, email=email, password=password)
        self.headers = get_authorized_header(self.query, username, password)

    def test_success(self):
        response = self.query(query=clock_in_query_str, headers=self.headers)

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
