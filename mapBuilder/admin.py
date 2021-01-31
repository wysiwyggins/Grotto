from django.contrib import admin


# Register your models here.
from .models import Room


""" class RoomInline(admin.ModelAdmin):
    model = Room
    extra = 4


class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name']}),
        ('URLField',               {'fields': ['url']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        (None,               {'fields': ['description']}),
    ]
    inlines = [RoomInline]
    list_display = ('name', 'url', 'pub_date', 'description')
    list_filter = ['pub_date']

admin.site.register(Room, RoomAdmin) """