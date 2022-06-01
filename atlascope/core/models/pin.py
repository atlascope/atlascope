from django.contrib import admin
from django.contrib.gis.db.models import PointField
from django.db import models
from django.db.models import CheckConstraint, F, Q
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
    location = PointField()
    color = models.CharField(
        max_length=15, choices=PIN_COLORS, default='red', null=False, blank=False
    )
    description = models.TextField(max_length=1000, blank=True)
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
    child = models.ForeignKey(
        'Dataset',
        on_delete=models.CASCADE,
        null=True,
        related_name='locations',
    )



class NotePinSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotePin
        fields = '__all__'


class DatasetPinSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetPin
        fields = '__all__'


class PinSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        try:
            notepin = instance.notepin
            return NotePinSerializer(notepin).data
        except:
            pass
        try:
            datasetpin = instance.datasetpin
            return DatasetPinSerializer(datasetpin).data
        except:
            pass
        return super().to_representation(instance)

    class Meta:
        model = Pin
        fields = '__all__'


class InvestigationPinSerializer(serializers.BaseSerializer):
    note_pins = NotePinSerializer(many=True)
    dataset_pins = DatasetPinSerializer(many=True)


@admin.register(Pin)
class PinAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'description')
