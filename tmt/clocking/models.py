from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Clock(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='clocking_logs', on_delete=models.CASCADE)
    clocked_in = models.DateTimeField(auto_now_add=True)
    clocked_out = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.user}: {self.clocked_in} - {self.clocked_out}'


class ActiveClocking(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='current_clock', primary_key=True,
                                on_delete=models.CASCADE)
    clock = models.OneToOneField(Clock, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}: {self.clock}'
