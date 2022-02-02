from graphene_django import DjangoObjectType

from tmt.clocking.models import Clock


class ClockType(DjangoObjectType):
    class Meta:
        model = Clock
        fields = ("id", "user", "clocked_in", "clocked_out")
