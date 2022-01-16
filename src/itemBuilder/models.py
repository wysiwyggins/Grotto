from datetime import timedelta

from django.db.models.fields import NullBooleanField
from colorfield.fields import ColorField
from django.db import models
from django.utils.timezone import now
from django_enumfield import enum
from mapBuilder.models import Room
from characterBuilder.models import Character, NonPlayerCharacter

from itemBuilder.enum import ItemType, ItemAction


class AbstractItem(models.Model):
    itemType = enum.EnumField(ItemType)
    itemName = models.CharField(max_length=64)
    itemDescription = models.CharField(max_length=256)

    active_time = models.DurationField(null=True, blank=True)
    untakable = models.BooleanField(default=False)
    untakable_if_active = models.BooleanField(default=False)
    holders = models.ManyToManyField(NonPlayerCharacter, related_name="loot", blank=True)
    viewable = models.BooleanField(default=False)
    usable = models.BooleanField(default=False)

    def __str__(self):
        return self.itemName


class Item(models.Model):
    name = models.CharField(max_length=128, default="blank")
    description = models.CharField(max_length=256, default="blank")
    abstract_item = models.ForeignKey(AbstractItem, on_delete=models.CASCADE)
    current_owner = models.ForeignKey(
        Character, on_delete=models.SET_NULL, null=True, blank=True, related_name="inventory"
    )
    current_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True, related_name="items"
    )
    active = models.DateTimeField(null=True, blank=True)
    colorName = models.CharField(max_length=200)
    colorHex = ColorField(default="#222222")

    def __str__(self):
        return self.name

    @property
    def is_takeable(self):
        if self.abstract_item.untakable:
            return False
        if self.active and self.abstract_item.untakable_if_active:
            return False
        return True

    @property
    def is_viewable(self):
        return self.abstract_item.viewable

    @property
    def is_active(self):
        if self.active is None:
            return False
        if self.abstract_item.active_time is None:
            return True
        if self.active > now() - self.abstract_item.active_time:
            return True
        return False

    @property
    def is_usable(self):
        return self.abstract_item.usable


class Swap(models.Model):
    # picks_up_item
    picks_type = enum.EnumField(ItemType)
    # drops_item
    puts = models.ForeignKey(AbstractItem, on_delete=models.PROTECT)
    # npc
    npc = models.ForeignKey(NonPlayerCharacter, on_delete=models.PROTECT)
    message = models.CharField(max_length=200)
