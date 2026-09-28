from django.db import models


class Booking(models.Model):
    room = models.CharField(max_length=20)
    start = models.DateTimeField()
    end = models.DateTimeField()
