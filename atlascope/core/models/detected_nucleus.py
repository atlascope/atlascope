from django.contrib import admin
from django.contrib.gis.db import models as geo_models
from django.db import models
from rest_framework import serializers

from atlascope.core.models.dataset import Dataset


class DetectedNucleus(models.Model):
    detection_dataset = models.ForeignKey(
        Dataset,
        null=False,
        on_delete=models.CASCADE,
        related_name='detected_nuclei',
    )
    label_integer = models.IntegerField()
    centroid = geo_models.PointField()
    weighted_centroid = geo_models.PointField()
    bounding_box = geo_models.PolygonField()
    orientation = models.FloatField()
    nucleus_gradient = models.JSONField()
    nucleus_haralick = models.JSONField()
    nucleus_intensity = models.JSONField()
    shape = models.JSONField()
    size = models.JSONField()


class DetectedNucleusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedNucleus
        fields = '__all__'


@admin.register(DetectedNucleus)
class DetectedNucleusAdmin(admin.ModelAdmin):
    list_display = ('id', 'detection_dataset')
