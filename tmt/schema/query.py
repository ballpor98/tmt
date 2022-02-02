import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from tmt.clocking.models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile


class Query(graphene.ObjectType):
    whoami = graphene.Field(UserType)
    users = graphene.List(UserType)

    @staticmethod
    def resolve_whoami(info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return user

    @staticmethod
    def resolve_users(info):
        user = info.context.user
        print(user)
        # Check to ensure user is a 'manager' to see all users
        if user.is_anonymous:
            raise Exception('Authentication Failure: Your must be signed in')
        return get_user_model().objects.all()