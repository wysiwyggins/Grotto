from rest_framework import serializers

from itemBuilder import models


class AbstractItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AbstractItem
        fields = ("pk", "itemName", "itemDescription")


class ItemSerializer(serializers.ModelSerializer):
    abstract_item = AbstractItemSerializer()
    class Meta:
        model = models.Item
        fields = ("pk", "abstract_item", "colorName", "colorHex", "is_active")