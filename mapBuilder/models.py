from django.db import models

# Create your models here.


class Room(models.Model):
    room_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
 #   url = 
 #   visits =
 #   exits
    pub_date = models.DateTimeField('date created')
    description = models.CharField(max_length=600)
#    color = 

class Visit(models.Model):
    visit_id = models.IntegerField(default=0)
    visitor_id = models.IntegerField(default=0)
    stamp_date = models.DateTimeField('date created')