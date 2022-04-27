from django.db import models


class TourWaypoints(models.Model):
    sequence = models.IntegerField(null=True)
    waypoint = models.ForeignKey('Waypoint', on_delete=models.CASCADE, null=True)
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, null=True)
