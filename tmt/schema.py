import graphene
from graphene_django import DjangoObjectType

from tmt.clocking.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username")


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user_by_username = graphene.Field(UserType, username=graphene.String(required=True))

    @staticmethod
    def resolve_all_users(root, info):
        return User.objects.all()

    @staticmethod
    def resolve_user_by_username(root, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)
