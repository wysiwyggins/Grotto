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
    pass


class ItemAction(enum.Enum):
    USE = 0
    GIVE = 1
    PLACE = 2
    TAKE = 3
    pass


class AbstractItem(models.Model):
    itemType = enum.EnumField(ItemType)
    itemName = models.CharField(max_length=64)
    itemDescription = models.CharField(max_length=256)
    pass


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


# service
class ItemService:
    def use(self, item, character):  # Item model instance
        # validate that the item type exists
        if candle:
            self._use_candle()
        pass

    def give(self, item, character, recipient):
        pass

    def _use_candle(self, item, character):
        pass

    def _use_scrubbrush(self, item, character):
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
