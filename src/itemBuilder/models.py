from datetime import timedelta

from django.db.models.fields import NullBooleanField
from colorfield.fields import ColorField
from django.db import models
from django.utils.timezone import now
from django_enumfield import enum
from mapBuilder.models import Room
from characterBuilder.models import Character

# Create your models here.


class ItemType(enum.Enum):
    CANDLE = 0
    SCRUBBRUSH = 1
    INCENSE = 2
    AMULET = 3
    PENTAGRAM = 4
    FECES = 5
    ARROW = 6



class ItemAction(enum.Enum):
    USE = 0
    GIVE = 1
    PLACE = 2
    TAKE = 3



class AbstractItem(models.Model):
    itemType = enum.EnumField(ItemType)
    itemName = models.CharField(max_length=64)
    itemDescription = models.CharField(max_length=256)

    active_days = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.itemName


class Item(models.Model):
    abstract_item = models.ForeignKey(AbstractItem, on_delete=models.CASCADE)
    current_owner = models.ForeignKey(
        Character, on_delete=models.SET_NULL, null=True, blank=True, related_name="character_items"
    )
    current_room = models.ForeignKey(
        Room, on_delete=models.CASCADE, null=True, blank=True, related_name="items"
    )
    active = models.DateTimeField(null=True, blank=True)
    colorName = models.CharField(max_length=200)
    colorHex = ColorField(default="#222222")

    @property
    def is_active(self):
        if self.active is None:
            return False
        if self.abstract_item.active_days is None:
            return True
        if self.active > now() - timedelta(days=self.abstract_item.active_days):
            return True
        return False


# service
class ItemService:
    def use(self, *, item, character):  # Item model instance
        # validate that the item type exists
        if item.abstract_item.itemType == ItemType.CANDLE:
            self._use_burnable(item, character)
        if item.abstract_item.itemType == ItemType.INCENSE:
            self._use_burnable(item, character)
            self.place(item, character)
        if item.abstract_item.itemType == ItemType.SCRUBBRUSH:
            self._use_scrubbrush(item, character)

    def place(self, item, character):
        item.current_owner = None
        item.current_room = character.room
        item.save()
        if item.abstract_item.itemType == ItemType.INCENSE and item.is_active:
            character.room.is_cursed = False
            character.room.save()

    def take(self, item, character):
        if item.abstract_item.itemType == ItemType.CANDLE and item.is_active:
            # cannot pick up an active candle
            return
        pass

    def give(self, item, character, recipient):
        pass

    def _use_burnable(self, item, character):
        if item.active:
            return
        item.active = now()
        item.save()

    def _use_scrubbrush(self, item, character):
        room = character.room
        room.cleanliness = min(2, room.cleanliness + 1)
        room.save()

    def _use_incense(self, item, character):
        pass

    def _use_amulet(self, item, character):
        pass


"""
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
    arrow_count = models.IntegerField(default=0)
    # video embeds
    hosted_video_link = models.URLField(max_length=200, blank=True)
    vimeo_id = models.CharField(max_length=200, blank=True)
    youtube_id = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ["id", "url"]

    def __str__(self):
        return self.name
 """
