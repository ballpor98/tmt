import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.utils import timezone

from tmt.clocking.models import Clock, CurrentClock
from tmt.clocking.schema.query import ClockType, UserType


class ClockIn(graphene.Mutation):
    clock = graphene.Field(ClockType)

    def mutate(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        if hasattr(user, 'currentclock'):
            raise Exception('Clcoking in Failure: Your already clocking in please clock out first')
        clock = Clock(user=user)
        clock.save()
        CurrentClock(user=user, clock=clock).save()
        return ClockIn(clock=clock)


class ClockOut(graphene.Mutation):
    clock = graphene.Field(ClockType)

    def mutate(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        if not hasattr(user, 'currentclock'):
            raise Exception('Clcoking out Failure: Please clock in first')
        clock = user.currentclock.clock
        clock.clocked_out = timezone.now()
        clock.save()
        user.currentclock.delete()
        return ClockOut(clock=clock)


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    clock_in = ClockIn.Field()
    clock_out = ClockOut.Field()
    create_user = CreateUser.Field()
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
