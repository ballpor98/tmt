import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token

from tmt.clocking.models import Profile
from tmt.schema.query import UserType, UserProfile


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


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()