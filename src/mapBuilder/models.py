import datetime

from colorfield.fields import ColorField
from django.db import models
from django.utils.timezone import now

# Create your models here.


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
    # illumination_level = models.IntegerField(default=0)
    # cleanliness_level = models.IntegerField(default=0)
    # sanctity_level = models.IntegerField(default=0)


    class Meta:
        unique_together = ["id", "url"]

    def __str__(self):
        return self.name
