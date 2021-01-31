from django.contrib import admin
from mapBuilder.models import Character

admin.site.register(Character)
# Register your models here.
from .models import Character