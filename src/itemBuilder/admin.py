from django.contrib import admin

from itemBuilder.models import (
    AbstractItem,
    Item,
    Swap,
)


@admin.register(AbstractItem)
class AbstractItemAdmin(admin.ModelAdmin):
    list_display = ("itemName", "itemType")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("abstract_item", "current_owner", "current_room")


@admin.register(Swap)
class SwapAdmin(admin.ModelAdmin):
    list_display = ("id", "picks_type", "puts", "npc")


