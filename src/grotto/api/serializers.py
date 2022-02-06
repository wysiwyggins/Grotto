from rest_framework import serializers

from mapBuilder.api.serializers import RoomSerializer
from characterBuilder.api.serializers import CharacterSerializer


class NullSerializer(serializers.Serializer):
    pass


class TableauSerializer(serializers.Serializer):
    character = CharacterSerializer()
    room = RoomSerializer()
    messages = serializers.ListField(child=serializers.CharField(), allow_empty=True)
