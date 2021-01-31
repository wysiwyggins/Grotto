import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class Character(models.Model):
    char_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    characterType = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created')
    description = models.TextField()
    def __str__(self):
        return self.name
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#   active = models.Bool(default=false)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
