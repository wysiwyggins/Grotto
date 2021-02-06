import datetime
from colorfield.fields import ColorField
from django.db import models
from django.utils import timezone
from characterBuilder.models import Character
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
 #  visits =
    exits = models.ManyToManyField('self', symmetrical=True)
    pub_date = models.DateTimeField('date created')
    description = models.CharField(max_length=600)
    colorName = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    colorHex = ColorField(default='#222222')
    class Meta:
        unique_together = ["id", "url"]
    def __str__(self):
        return self.name


""" class Visit(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    stamp_date = models.DateTimeField('date created') """