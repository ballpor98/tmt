from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Clock(models.Model):
    user = models.ForeignKey(User, related_name='clocking_logs', on_delete=models.CASCADE)
    clocked_in = models.DateTimeField(auto_now_add=True)
    clocked_out = models.DateTimeField()

    def __str__(self):
        return self.name
