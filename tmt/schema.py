import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.shortcuts import get_token
import graphene

from tmt.clocking.models import Profile


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class UserProfile(DjangoObjectType):
    class Meta:
        model = Profile


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    profile = graphene.Field(UserProfile)
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @staticmethod
    def mutate(info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        profile_obj = Profile.objects.get(user=user.id)
        token = get_token(user)

        return CreateUser(user=user, profile=profile_obj, token=token)


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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
