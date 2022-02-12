from rest_framework import serializers

from characterBuilder import models
from itemBuilder.api.serializers import ItemSerializer


class OccupantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Character
        fields = ("pk", "kind", "name")


class NonPlayerCharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NonPlayerCharacter
        fields = ("pk", "name", "greeting")


class CharacterSerializer(serializers.ModelSerializer):
    inventory = ItemSerializer(many=True)

    class Meta:
        model = models.Character
        fields = ("pk", "kind", "name", "description", "inventory", "arrow_count")


class RoomVisitSerializer(serializers.ModelSerializer):
    character = OccupantSerializer()

    class Meta:
        model = models.Visit
        fields = ("character", "stamp_date", "died_here")
