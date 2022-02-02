from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from tmt.clocking.models import User, Clock, CurrentClock


class ClockAdmin(admin.ModelAdmin):
    list_display = ('user', 'clocked_in', 'clocked_out')


class CurrentClockAdmin(admin.ModelAdmin):
    list_display = ('user', 'clock')


admin.site.register(User, UserAdmin)
admin.site.register(Clock, ClockAdmin)
admin.site.register(CurrentClock, CurrentClockAdmin)
