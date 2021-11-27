from django.contrib import admin

from itemBuilder.models import (
    AbstractItem,
    Item,
)


@admin.register(AbstractItem)
class AbstractItemAdmin(admin.ModelAdmin):
    list_display = ("itemName", "itemType")
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("abstract_item", "current_owner", "current_room")
    pass


