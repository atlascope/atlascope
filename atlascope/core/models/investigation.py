from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django_extensions.db.models import TimeStampedModel

from uuid import uuid4

from atlascope.core.models import ConnectionsMap, ContextMap


class Investigation(TimeStampedModel, models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, null=False)
    collaborators = models.ManyToManyField(User, related_name="collaborators")
    observers = models.ManyToManyField(User, related_name="observers")
    context_map = models.ForeignKey('ContextMap', on_delete=models.PROTECT, editable=False)
    connections_map = models.ForeignKey('ConnectionsMap', on_delete=models.PROTECT, editable=False)

    def save(self, *args, **kwargs):
        # enforce creation of maps for this investigation
        if not self.context_map:
            new_context_map = ContextMap()
            new_context_map.save()
            self.context_map = new_context_map
        if not self.connections_map:
            new_connections_map = ConnectionsMap()
            new_connections_map.save()
            self.connections_map = new_connections_map
        super().save(*args, **kwargs)


@admin.register(Investigation)
class InvestigationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    list_filter = ('created', 'modified', 'owner')
