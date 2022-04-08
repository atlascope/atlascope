from uuid import uuid4

from django.db import models
from rest_framework import serializers


class Tour(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    way_points = models.ManyToManyField('Waypoint', through='Tour_waypoints')


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
