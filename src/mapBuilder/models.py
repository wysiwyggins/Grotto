import datetime
from colorfield.fields import ColorField
from django.db import models
import datetime
from django.utils.timezone import now
# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True)
 #  visits =
    exits = models.ManyToManyField('self', symmetrical=True)
    pub_date = models.DateTimeField(default=now,blank=True)
    # PS: Possibly use a TextField for description unless you're sure that
    #  the generator will come in under 600 chars
    description = models.TextField()
    colorName = models.CharField(max_length=200)
    status = models.CharField(max_length=200, blank=True)
    colorHex = ColorField(default='#222222')
    colorSlug = models.SlugField(null=True)

    class Meta:
        unique_together = ["id", "url"]
    def __str__(self):
        return self.name
