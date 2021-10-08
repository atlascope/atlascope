from uuid import uuid4

from django.contrib import admin
from django.db import models


class ConnectionsMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pins = models.ManyToManyField('Pin', related_name='connection_pins')
    # connections
    notes = models.TextField(max_length=5000, blank=True)


@admin.register(ConnectionsMap)
class ContextMapAdmin(admin.ModelAdmin):
    pass
