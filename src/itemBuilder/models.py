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

    active_days = models.IntegerField(null=True, blank=True)
    untakable = models.BooleanField(default=False)
    untakable_if_active = models.BooleanField(default=False)
    holders = models.ManyToManyField(NonPlayerCharacter, related_name="loot", blank=True)

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

    @property
    def is_takeable(self):
        if self.abstract_item.untakable:
            return False
        if self.active and self.abstract_item.untakable_if_active:
            return False
        return True

    @property
    def is_active(self):
        if self.active is None:
            return False
        if self.abstract_item.active_days is None:
            return True
        if self.active > now() - timedelta(days=self.abstract_item.active_days):
            return True
        return False
