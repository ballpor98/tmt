from datetime import datetime, timedelta
from typing import List

import graphene
from django.contrib.auth import get_user_model
from django.utils import timezone
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


def get_first_week_day(today) -> datetime:
    # assume that start from monday
    day_num = timedelta(days=today.weekday())
    return today - day_num


def get_clocked_hours(clocks: List[Clock]) -> int:
    timedelta_list = [(clock.clocked_out - clock.clocked_in) for clock in clocks]
    total_seconds = sum(timedelta_list, timedelta()).total_seconds()
    total_hours = round(total_seconds / 3600.)
    return int(total_hours)


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
        # care timezone
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        this_week = get_first_week_day(today)
        this_month = today.replace(day=1)

        # count from clocked_in datetime
        month_clocks = Clock.objects.filter(clocked_in__gte=this_month)
        week_clocks = Clock.objects.filter(clocked_in__gte=this_week)
        today_clocks = week_clocks.filter(clocked_in__gte=today)

        month_clocked = get_clocked_hours(month_clocks)
        week_clocked = get_clocked_hours(week_clocks)
        today_clocked = get_clocked_hours(today_clocks)
        return ClockedHours(today=today_clocked, current_week=week_clocked, current_month=month_clocked)
