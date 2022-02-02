import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from tmt.clocking.models import Clock, ActiveClocking
from tmt.utils import check_auth


class ClockType(DjangoObjectType):
    class Meta:
        model = Clock
        fields = ("id", "user", "clocked_in", "clocked_out")


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email")


class CurrentClock(DjangoObjectType):
    class Meta:
        model = ActiveClocking
        fields = ("clock",)


class ClockedHours(graphene.ObjectType):
    today = graphene.Int()
    current_week = graphene.Int()
    current_month = graphene.Int()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    current_clock = graphene.Field(CurrentClock)
    clocked_hours = graphene.Field(ClockedHours)

    def resolve_me(self, info):
        user = info.context.user
        check_auth(user)
        return user

    def resolve_current_clock(self, info):
        user = info.context.user
        check_auth(user)
        if not hasattr(user, 'current_clock'):
            raise Exception('Query currentClock Failure: Not have any currentClock now')
        return user.current_clock

    def resolve_clocked_hours(self, info):
        user = info.context.user
        check_auth(user)
        return ClockedHours(today=1, current_week=2, current_month=3)
