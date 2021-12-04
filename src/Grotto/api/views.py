from rest_framework import generics
from rest_framework.response import Response
from django.contrib.messages import get_messages

# from mapBuilder import models
from Grotto.api import serializers

class TableauView(generics.GenericAPIView):
    serializer_class = serializers.TableauSerializer

    def get(self, request, *args, **kwargs):

        serializer = serializers.TableauSerializer(
            {
                "character": request.character,
                "room": request.character.room,
                "messages": [str(m) for m in get_messages(request)]
            }
        )
        # serializer.is_valid()
        return Response(serializer.data)
