from datetime import timedelta

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

    def warnings(self):
        _warnings = []
        for exit in self.exits.all().prefetch_related("npcs").order_by("?"):
            _warnings.extend(exit.npcs.all().values_list("warning_text", flat=True))
        # ensure that the warnings are in a random order so that the
        return _warnings

    @property
    def visits(self):
        deduped_visits = []
        visitors = []
        visits = (
            self._visits.all().filter(room=self)
            .exclude(stamp_date__lt=now() - timedelta(days=7))
            .order_by("-stamp_date")
        )
        for visit in visits:
            if visit.character not in visitors:
                deduped_visits.append(visit)
                visitors.append(visit.character)
        return deduped_visits


class Cenotaph(models.Model):
    room = models.OneToOneField(Room, on_delete=models.PROTECT, related_name="cenotaph")
    text = models.TextField(help_text="The inscription on the cenotaph")
    name = models.CharField(max_length=64)
    birth = models.CharField(max_length=32, null=True, blank=True)
    death = models.CharField(max_length=32, null=True, blank=True)
    scene = models.TextField(help_text="This 'a-frame' will be inserted in the cenotaph as background", null=True, blank=True)
    portrait_filename = models.CharField(max_length=64, null=True, blank=True)
    # TODO: get S3 uploads sorted out
    # portrait = models.FileField()


class RoomEvent(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="events")
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=256)


# Eventually!
# class CenotaphFileUpload(models.Model):
#     file = models.FileField(...)
