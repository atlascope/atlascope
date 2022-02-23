from uuid import uuid4

from django.contrib import admin
from django.contrib.gis.db.models import PointField
from django.db import models
from rest_framework import serializers

PIN_COLORS = [
    ('red', 'red'),
    ('blue', 'blue'),
    ('green', 'green'),
    ('orange', 'orange'),
    ('purple', 'purple'),
    ('black', 'black'),
]


class Pin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    color = models.CharField(
        max_length=15, choices=PIN_COLORS, default='red', null=False, blank=False
    )
    parent_dataset = models.ForeignKey('Dataset', on_delete=models.CASCADE, related_name='pins')
    child_dataset = models.ForeignKey(
        'Dataset', on_delete=models.CASCADE, null=True, related_name='locations'
    )
    location = PointField()
    note = models.TextField(max_length=1000, blank=True)


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'note')
