from rest_framework import generics
from rest_framework.response import Response
from django.contrib.messages import get_messages

# from mapBuilder import models
from Grotto.api import serializers

class TableauAPIView(generics.GenericAPIView):
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



class EnterAPIView(generics.GenericAPIView):
    pass
class MoveAPIView(generics.GenericAPIView):
    pass
class FireArrowAPIView(generics.GenericAPIView):
    pass
class BecomeCharacterAPIView(generics.GenericAPIView):
    pass
class UseItemAPIView(generics.GenericAPIView):
    pass
class TakeItemAPIView(generics.GenericAPIView):
    pass
class PlaceItemAPIView(generics.GenericAPIView):
    pass
class DropItemAPIView(generics.GenericAPIView):
    pass
class ViewItemAPIView(generics.GenericAPIView):
    pass