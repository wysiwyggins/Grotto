from django.contrib import admin

from itemBuilder.models import (
    AbstractItem,
    Item,
)


@admin.register(AbstractItem)
class AbstractItemAdmin(admin.ModelAdmin):
    # list_display = ()
    pass


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    # list_display = ()
    pass


