from uuid import uuid4

from django.contrib import admin
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
    dataset = models.ForeignKey('Dataset', on_delete=models.PROTECT)
    color = models.CharField(
        max_length=15, choices=PIN_COLORS, default='red', null=False, blank=False
    )
    # pin_location
    note = models.TextField(max_length=1000, blank=True)


class PinSerializer(serializers.ModelSerializer):
    dataset = serializers.SerializerMethodField('get_dataset')

    def get_dataset(self, obj):
        return None

    class Meta:
        model = Pin
        fields = '__all__'


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'dataset', 'color', 'note')
