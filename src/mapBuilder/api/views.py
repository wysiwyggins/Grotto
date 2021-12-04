from rest_framework import generics

from mapBuilder import models
from mapBuilder.api import serializers

class RoomView(generics.RetrieveAPIView):
    lookup_url_kwarg = "pk"
    queryset = models.Room.objects.all()
    serializer_class = serializers.RoomSerializer
