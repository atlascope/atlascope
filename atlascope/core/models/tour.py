from django.contrib import admin
from django.db import models
from rest_framework import serializers


class Tour(models.Model):
    name = models.CharField(max_length=255, default='My Tour')
    waypoints = models.ManyToManyField('Waypoint', through='TourWaypoints')
    # investion fk like pins


admin.site.register(Tour)


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'
