from uuid import uuid4

from django.contrib import admin
from django.db import models
from rest_framework import serializers


class ConnectionsMap(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pins = models.ManyToManyField('Pin', related_name='connection_pins')
    # connections
    notes = models.TextField(max_length=5000, blank=True)


class ConnectionsMapSerializer(serializers.HyperlinkedModelSerializer):
    pins = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='pin-detail')

    class Meta:
        model = ConnectionsMap
        fields = '__all__'


@admin.register(ConnectionsMap)
class ContextMapAdmin(admin.ModelAdmin):
    pass
