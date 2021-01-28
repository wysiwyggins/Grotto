import datetime

from django.db import models
from django.utils import timezone
from characterBuilder.models import Character
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
 #   visits =
    exits = models.URLField(max_length=200)
    pub_date = models.DateTimeField('date created')
    description = models.CharField(max_length=600)
#   color = 
    class Meta:
        unique_together = ["id", "url"]


class Visit(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    stamp_date = models.DateTimeField('date created')