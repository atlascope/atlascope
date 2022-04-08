from uuid import uuid4

from django.db import models


class Tour_waypoints(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sequence = models.IntegerField(null=True)
    way_point = models.ForeignKey('Waypoint', on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True)
