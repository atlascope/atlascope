from drf_yasg import openapi
from django.contrib import admin
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import CheckConstraint, F, Q
from polymorphic.models import PolymorphicModel
from rest_framework import serializers
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


class BasePinSerializer(serializers.ModelSerializer):
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


class PinSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        Pin: BasePinSerializer,
        NotePin: NotePinSerializer,
        DatasetPin: DatasetPinSerializer,
    }

    class Meta:
        swagger_schema_fields = {
            'type': openapi.TYPE_OBJECT,
            'title': 'Pin',
            'required': [
                'id',
                'investigation',
                'parent',
                'minimum_zoom',
                'maximum_zoom',
                'resource_type',
                'location',
                'color',
            ],
            'properties': {
                'id': openapi.Schema(
                    title='id',
                    type=openapi.TYPE_INTEGER
                ),
                'investigation': openapi.Schema(
                    title='investigation',
                    type=openapi.TYPE_INTEGER
                ),
                'parent': openapi.Schema(
                    title='parent',
                    type=openapi.TYPE_INTEGER
                ),
                'minimum_zoom': openapi.Schema(
                    title='minimum_zoom',
                    type=openapi.TYPE_INTEGER
                ),
                'maximum_zoom': openapi.Schema(
                    title='maximum_zoom',
                    type=openapi.TYPE_INTEGER
                ),
                'location': openapi.Schema(
                    title='location',
                    type=openapi.TYPE_STRING
                ),
                'color': openapi.Schema(
                    title='color',
                    type=openapi.TYPE_STRING
                ),
                'resource_type': openapi.Schema(
                    title='resource_type',
                    type=openapi.TYPE_STRING
                ),
                'description': openapi.Schema(
                    title='description',
                    type=openapi.TYPE_STRING
                ),
                'note': openapi.Schema(
                    title='note',
                    type=openapi.TYPE_STRING
                ),
                'child': openapi.Schema(
                    title='child',
                    type=openapi.TYPE_INTEGER
                )
            }
        }


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'color')
