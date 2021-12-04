from rest_framework import serializers

from mapBuilder import models
from characterBuilder.api.serializers import OccupantSerializer, NonPlayerCharacterSerializer
from itemBuilder.api.serializers import ItemSerializer



class ExitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ("pk", "name", "colorSlug", "colorHex")


class RoomAttributeSerializer(serializers.Serializer):
    brightness = serializers.IntegerField()
    cleanliness = serializers.IntegerField()
    sanctity = serializers.IntegerField()


class RoomSerializer(serializers.ModelSerializer):
    exits = ExitSerializer(many=True)
    occupants = OccupantSerializer(many=True)
    npcs = NonPlayerCharacterSerializer(many=True)
    items = ItemSerializer(many=True)
    attributes = RoomAttributeSerializer(source="get_attributes")

    def get_attributes(self, obj):
        return RoomAttributeSerializer(RoomService().get_attributes(obj))

    class Meta:
        model = models.Room
        fields = (
            "name",
            "colorName",
            "colorHex",
            "description",
            "exits",
            "occupants",
            "npcs",
            "items",
            "attributes",
        )


