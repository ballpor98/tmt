import json

from graphene_django.utils.testing import GraphQLTestCase

from tests.test_clock_in import clock_in_query_str
from tests.test_clock_out import clock_out_query_str
from tests.utils import get_authorized_header
from tmt.clocking.models import User

GraphQLTestCase.GRAPHQL_URL = '/graphql'

clocked_hours_query_str = (
    '''
    query getCurrentClock{
        clockedHours{
            today
            currentWeek
            currentMonth
        }
    }
    '''
)


class ClockedHoursTestCase(GraphQLTestCase):
    def setUp(self):
        username = 'janedoe'
        email = 'j.doe@test'
        password = 'top_secret'
        self.user = User.objects.create_user(
            username=username, email=email, password=password)
        self.headers = get_authorized_header(self.query, username, password)

    def test_success(self):
        self.query(query=clock_in_query_str, headers=self.headers)
        self.query(query=clock_out_query_str, headers=self.headers)
        response = self.query(query=clocked_hours_query_str, headers=self.headers)

        content = json.loads(response.content)

        self.assertResponseNoErrors(response)
