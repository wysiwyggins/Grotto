import datetime

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from mapBuilder.models import Room


class User(AbstractUser):
    """Placeholder User model in case we need to add fields in the future
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/...
      #using-a-custom-user-model-when-starting-a-project
    """
    accepts_terms = models.BooleanField(default=False)


class Character(models.Model):
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField('date created', default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="occupants")
    arrow_count = models.IntegerField(default=1)
    dead = models.BooleanField(default=False)
    deathnote = models.CharField(max_length=200, null=True, blank=True)
    # player_character = models.BooleanField(default=False)
    # active = models.Bool(default=false)

    def __str__(self):
        return self.name

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class NonPlayerCharacter(models.Model):
    name = models.CharField(max_length=200)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, related_name="occupants")
    mobile = models.BooleanField(default=True)
    deadly = models.BooleanField(default=True)
    mortal = models.BooleanField(default=True)
    movement_entropy = models.IntegerField(
        default=0, help_text="See Movement Threshold")
    movement_threshold = models.IntegerField(
        default=100,
        help_text="When Movement Entropy exceeds this threshold the NPC will move")


class Skill(models.Model):
    name = models.CharField(max_length=50)
    level = models.IntegerField()
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='skills')


class Item(models.Model):
    name = models.CharField(max_length=50)
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='items')


class CharacterTest(models.Model):
    question = models.CharField(max_length=2000)


class CharacterTestChoice(models.Model):
    character_test = models.ForeignKey(CharacterTest, on_delete=models.CASCADE, related_name='choices')
    choice = models.CharField(max_length=400)


class Visit(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    stamp_date = models.DateTimeField('date created', default=timezone.now)
    died_here = models.BooleanField(default=False)
