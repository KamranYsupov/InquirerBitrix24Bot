from django.contrib import admin

from .models import Deal, ScheduledTask


admin.site.register(Deal)
admin.site.register(ScheduledTask)