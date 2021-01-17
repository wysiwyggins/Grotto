import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Character(models.Model):
    char_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created')
    description = models.CharField(max_length=600)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#   active = models.Bool(default=false)
    user_id = models.IntegerField(default=0)


class Skill(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=200)
    points = models.IntegerField(default=0)
    def __str__(self):
        return self.skill_name