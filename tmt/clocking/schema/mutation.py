import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphql_jwt.shortcuts import get_token

from tmt.clocking.schema.user import UserType


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()

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

        token = get_token(user)

        return CreateUser(user=user, token=token)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
