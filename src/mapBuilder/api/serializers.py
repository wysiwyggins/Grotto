from rest_framework import serializers

from mapBuilder import models
from characterBuilder.api.serializers import (
    NonPlayerCharacterSerializer,
    OccupantSerializer,
    RoomVisitSerializer,
)
from itemBuilder.api.serializers import ItemSerializer


class ExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ("pk", "name", "colorSlug", "colorHex")


class RoomAttributeSerializer(serializers.Serializer):
    brightness = serializers.IntegerField()
    cleanliness = serializers.IntegerField()
    sanctity = serializers.IntegerField()


class CenotaphSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cenotaph
        fields = ("pk", "name", "birth", "death", "text",)


class RoomSerializer(serializers.ModelSerializer):
    exits = ExitSerializer(many=True, read_only=True)
    occupants = OccupantSerializer(many=True, read_only=True)
    npcs = NonPlayerCharacterSerializer(many=True, read_only=True)
    items = ItemSerializer(many=True, read_only=True, source="visible_items")
    attributes = RoomAttributeSerializer(source="get_attributes", read_only=True)
    visits = RoomVisitSerializer(many=True, read_only=True)
    cenotaph = CenotaphSerializer(read_only=True, required=False)
    warnings = serializers.ListField(child=serializers.CharField(), read_only=True)

    def get_attributes(self, obj):
        return RoomAttributeSerializer(RoomService().get_attributes(obj))

    class Meta:
        model = models.Room
        fields = (
            "pk",
            "name",
            "colorName",
            "colorSlug",
            "colorHex",
            "description",
            "exits",
            "occupants",
            "npcs",
            "items",
            "visits",
            "cenotaph",
            "attributes",
            "warnings",
        )
