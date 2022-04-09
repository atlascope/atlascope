from django.contrib.gis.db import models as gisModels
from django.db import models


class Waypoint(models.Model):
    location = gisModels.PointField(null=True)
    zoom = models.IntegerField(null=True)
