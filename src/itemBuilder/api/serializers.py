from rest_framework import serializers

from itemBuilder import models
from django_enumfield.contrib.drf import NamedEnumField
from itemBuilder.enum import ItemType


class AbstractItemSerializer(serializers.ModelSerializer):
    itemType = NamedEnumField(ItemType)

    class Meta:
        model = models.AbstractItem
        fields = ("pk", "itemName", "itemDescription", "itemType")


class ItemSerializer(serializers.ModelSerializer):
    abstract_item = AbstractItemSerializer(read_only=True)

    class Meta:
        model = models.Item
        fields = (
            "pk",
            "name",
            "abstract_item",
            "colorName",
            "colorHex",
            "is_active",
            "is_usable",
            "is_takeable",
        )
