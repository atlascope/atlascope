from uuid import uuid4

from django.contrib.gis.db import models as gisModels
from django.db import models


class Waypoint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    location = gisModels.PointField(null=True)
    zoom = models.IntegerField(null=True)
