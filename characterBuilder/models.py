import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Placeholder User model in case we need to add fields in the future
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/...
      #using-a-custom-user-model-when-starting-a-project
    """
    pass


class Character(models.Model):
    char_id = models.IntegerField(default=0)
    characterName = models.CharField(max_length=200)
    characterSkills = models.CharField(max_length=200)
    characterType = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created')
    characterDescription = models.TextField()
    def __str__(self):
        return self.characterName
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#   active = models.Bool(default=false)
#   skills = ???
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
