from django.contrib import admin
from . import models


@admin.register(models.Instance)
class InstanceModel(admin.ModelAdmin):
    list_display = ['id', 'state', 'created_on', 'updated_on']
    list_filter = ['state']
    search_fields = ['id']
