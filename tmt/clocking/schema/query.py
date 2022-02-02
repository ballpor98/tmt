import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from tmt.clocking.models import Clock


class ClockType(DjangoObjectType):
    class Meta:
        model = Clock
        fields = ("id", "user", "clocked_in", "clocked_out")


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user
