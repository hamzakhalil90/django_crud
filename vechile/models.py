from django.db import models
from utils.reusable_classes import TimeStamps


class Make(TimeStamps):
    name = models.CharField(max_length=100)

class Vechile(TimeStamps):
    name = models.CharField(max_length=100)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    model = models.IntegerField()
    color = models.CharField(max_length=100)


