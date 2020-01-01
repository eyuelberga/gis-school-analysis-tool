from django.contrib.gis.db import models


class School(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    