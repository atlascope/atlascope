from django.db import models
from rest_framework import serializers


class Tour(models.Model):
    way_points = models.ManyToManyField('Waypoint', through='TourWaypoints')


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
