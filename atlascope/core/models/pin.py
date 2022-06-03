from drf_yasg import openapi
from django.contrib import admin
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import CheckConstraint, F, Q
from rest_framework import serializers
from polymorphic.models import PolymorphicModel
from rest_polymorphic.serializers import PolymorphicSerializer

PIN_COLORS = [
    ('red', 'red'),
    ('blue', 'blue'),
    ('green', 'green'),
    ('orange', 'orange'),
    ('purple', 'purple'),
    ('black', 'black'),
]


class Pin(PolymorphicModel):
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
    location = PointField()
    color = models.CharField(
        max_length=15, choices=PIN_COLORS, default='red', null=False, blank=False
    )
    minimum_zoom = models.PositiveIntegerField(default=0)
    maximum_zoom = models.PositiveIntegerField(default=40)

    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(maximum_zoom__gte=F('minimum_zoom')),
                name='valid_zoom_range',
            )
        ]


class NotePin(Pin):
    note = models.TextField(max_length=1000)


class DatasetPin(Pin):
    description = models.TextField(max_length=1000, blank=True)
    child = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        null=True,
        related_name='locations',
    )


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pin
        fields = '__all__'


class NotePinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotePin
        fields = '__all__'


class DatasetPinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetPin
        fields = '__all__'


class PinPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Pin: PinSerializer,
        NotePin: NotePinSerializer,
        DatasetPin: DatasetPinSerializer,
    }


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'color')
