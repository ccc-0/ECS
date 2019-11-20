from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Alarm_type)
admin.site.register(Alarm_level)
admin.site.register(alarm_management)

