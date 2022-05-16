from django.contrib import admin
from django.db import models
from atlascope.core.models.waypoint import Waypoint
from rest_framework import serializers


class Tour(models.Model):
    name = models.CharField(max_length=255, default='My Tour')
    waypoints = models.ManyToManyField('Waypoint', through='TourWaypoints')
    investigation = models.ForeignKey(
        'Investigation',
        on_delete=models.CASCADE,
        related_name='tours',
    )


admin.site.register(Tour)


class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = '__all__'


class TourSerializer(serializers.ModelSerializer):
    waypoints = WaypointSerializer(many=True)

    class Meta:
        model = Tour
        fields = '__all__'
