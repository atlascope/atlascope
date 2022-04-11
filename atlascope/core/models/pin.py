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
    investigation = models.ForeignKey(
        'Investigation',
        on_delete=models.CASCADE,
        related_name='pins',
    )
    parent = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        related_name='pins',
    )
    child = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        null=True,
        related_name='locations',
    )
    child_location = PointField()
    color = models.CharField(
        max_length=15, choices=PIN_COLORS, default='red', null=False, blank=False
    )
    note = models.TextField(max_length=1000, blank=True)


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'note')
