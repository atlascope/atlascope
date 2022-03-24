# from typing import List
from uuid import uuid4
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models as gisModels

from django.db import models
from rest_framework import serializers


class Tour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    investigation = models.ForeignKey(
        'Investigation',
        on_delete=models.CASCADE,
        related_name='tour',
    )
    way_points = ArrayField(
        ArrayField(
            gisModels.PointField(null=True),
            null=True
        ),
        null=True
    )


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestigationTour
        fields = '__all__'


class TourCreateSerializer(serializers.Serializer):
    way_points = serializers.ListField(child=serializers.ListField(child=serializers.IntegerField()))
