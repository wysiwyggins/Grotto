from django.contrib import admin

from mapBuilder import models

admin.site.register(models.Room)


class CenotaphFileInline(admin.StackedInline):
    fields = ("file",)
    model = models.CenotaphFile


@admin.register(models.Cenotaph)
class CenotaphAdmin(admin.ModelAdmin):
    list_display = ("name", "room")
    inlines = (CenotaphFileInline,)
