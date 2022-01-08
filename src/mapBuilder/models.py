import datetime

from colorfield.fields import ColorField
from django.db import models
from django.utils.timezone import now

from itemBuilder.enum import ItemType


class Room(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True)
    exits = models.ManyToManyField("self", symmetrical=True)
    pub_date = models.DateTimeField(default=now, blank=True)
    description = models.TextField()
    colorName = models.CharField(max_length=200)
    status = models.CharField(max_length=200, blank=True)
    colorHex = ColorField(default="#222222")
    colorSlug = models.SlugField(null=True)
    # video embeds
    hosted_video_link = models.URLField(max_length=200, blank=True)
    vimeo_id = models.CharField(max_length=200, blank=True)
    youtube_id = models.CharField(max_length=200, blank=True)
    cleanliness = models.IntegerField(default=1)
    is_cursed = models.BooleanField(default=False)

    class Meta:
        unique_together = ["id", "url"]

    def __str__(self):
        return self.name

    def _room_level(self, *, item_type):
        # check items in room
        _item = self.items.filter(abstract_item__itemType=item_type, active__isnull=False)

        active_item_count = sum([1 for candle in _item if candle.is_active])
        # active_item_count = 1
        if active_item_count > 0:
            return 2
        # check characters in self
        for character in self.occupants.all():
            # see if character has a candle
            _item = character.inventory.filter(abstract_item__itemType=item_type, active__isnull=False)
            active_item_count = sum([1 for candle in _item if candle.is_active])
            if active_item_count > 0:
                return 1
        return 0

    def get_attributes(self):
        sanctity = 0
        if not self.is_cursed:
            sanctity = self._room_level(item_type=ItemType.INCENSE)
        return {
            "cleanliness": self.cleanliness,
            "brightness": self._room_level(item_type=ItemType.CANDLE),
            "sanctity": sanctity,
        }