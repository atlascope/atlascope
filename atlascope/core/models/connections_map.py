from django.db import models
from django.contrib import admin

from uuid import uuid4


class ConnectionsMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pins = models.ManyToManyField('Pin', related_name='connection_pins')
    # connections
    notes = models.TextField(max_length=5000, blank=True)


@admin.register(ConnectionsMap)
class ContextMapAdmin(admin.ModelAdmin):
    pass
