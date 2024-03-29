import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

from mapBuilder.models import Room


class User(AbstractUser):
    """Placeholder User model in case we need to add fields in the future
    https://docs.djangoproject.com/en/3.1/topics/auth/customizing/...
      #using-a-custom-user-model-when-starting-a-project
    """

    accepts_terms = models.BooleanField(default=False)


class NamedModel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Character(NamedModel):
    kind = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.DateTimeField("date created", default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, null=True, blank=True, related_name="occupants"
    )
    arrow_count = models.IntegerField(default=1)
    dead = models.BooleanField(default=False)
    deathnote = models.CharField(max_length=200, null=True, blank=True)
    items = models.ManyToManyField("Item", blank=True)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class NonPlayerCharacter(NamedModel):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="npcs")
    mobile = models.BooleanField(default=True)
    deadly = models.BooleanField(default=True)
    mortal = models.BooleanField(default=True)
    movement_entropy = models.IntegerField(
        default=0, help_text="See Movement Threshold"
    )
    movement_threshold = models.IntegerField(
        default=100,
        help_text="When Movement Entropy exceeds this threshold the NPC will move",
    )
    warning_text = models.CharField(max_length=200)
    loot = models.ManyToManyField("Item", blank=True)


class Skill(NamedModel):
    level = models.IntegerField()
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="skills"
    )


class Item(NamedModel):
    # permissions = ...
    # Eventually items could imbue the carrier with some special powers which
    #   can be faciliated using django permissions.
    persistent = models.BooleanField(default=True)


class CharacterTest(models.Model):
    question = models.CharField(max_length=2000)


class CharacterTestChoice(models.Model):
    character_test = models.ForeignKey(
        CharacterTest, on_delete=models.CASCADE, related_name="choices"
    )
    choice = models.CharField(max_length=400)


class Visit(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, null=True)
    stamp_date = models.DateTimeField("date created", default=timezone.now)
    died_here = models.BooleanField(default=False)
