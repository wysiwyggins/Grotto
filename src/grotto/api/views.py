from django.contrib import messages
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from grotto.api import serializers
from grotto.game.services import (
    ItemService,
    GameService,
    PlayerCharacterService,
    GrottoGameWarning,
)
from characterBuilder.api.serializers import CharacterSerializer
from characterBuilder.models import Character, Visit
from mapBuilder.api.serializers import RoomSerializer
from mapBuilder.models import Room
from itemBuilder.api.serializers import ItemSerializer
from itemBuilder.models import Item


class TableauSerializerMixin:
    def get_tableau_serializer(self):
        return serializers.TableauSerializer(
            {
                "character": self.request.character,
                "room": self.request.character.room,
                "messages": [str(m) for m in messages.get_messages(self.request)],
            }
        )


class TableauAPIView(generics.GenericAPIView, TableauSerializerMixin):
    serializer_class = serializers.TableauSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_tableau_serializer()
        # serializer.is_valid()
        return Response(serializer.data)


class GameActionMixin(TableauSerializerMixin):
    """
    Always use this as the first parent class for any game action view or viewset.
    It handles:
      * breaking the sour news to a player that their character is dead,
      * standardizing the response json to a game action
      * resolving actions (e.g. rolling for npc movement)
    """

    def dispatch(self, request, *args, **kwargs):
        self.dice_count = 0
        if request.character is None:
            raise GrottoGameWarning("Character does not exist")
        # is this character alive
        if request.character.dead:
            # message about death
            messages.add_message(request, messages.INFO, request.character.deathnote)
            # Shortcut whatever action was requested because the player is dead!
            return self.finalize_response(request, None, *args, **kwargs)
        try:
            response = super().dispatch(request, *args, **kwargs)
        except GrottoGameWarning as e:
            self.dice_count = 0
            messages.add_message(request, messages.INFO, f"{e}")
            response = self.finalize_response(request, None, *args, **kwargs)
        return response

    def finalize_response(self, request, response, *args, **kwargs):
        self.advance_game()
        response = Response(self.get_tableau_serializer().data)
        return super().finalize_response(request, response, *args, **kwargs)

    def advance_game(self):
        # TODO: make burnable_swap a scheduled task
        ItemService().burnable_swap()
        if self.dice_count == 0:
            return
        game = GameService()
        # roll for dirtying room
        game.roll_to_dirty_room(
            room=self.request.character.room, dice_count=self.dice_count
        )
        # roll for NPC movements
        service_return = game.roll_to_move_npcs(dice_count=self.dice_count)
        # send messages
        for message in service_return.messages:
            messages.add_message(self.request, messages.INFO, message)


class EnterAPIView(GameActionMixin, generics.GenericAPIView):
    serializer_class = serializers.NullSerializer

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    def post(self, request, *args, **kwargs):
        if request.character.room is None:
            # choose a random, but safe room to enter
            request.character.room = Room.objects.exclude(
                npcs__deadly=True).order_by("?")[0]
            request.character.save()


class RoomViewSet(GameActionMixin, viewsets.GenericViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def move(self, request, pk):
        service_return = PlayerCharacterService().move(
            character=request.character, id=pk)
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)
        self.dice_count += 1

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def fire_arrow(self, request, pk):
        service_return = PlayerCharacterService().fire_arrow(
            character=request.character, id=pk)
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)
        self.dice_count += 5


class CharacterViewSet(GameActionMixin, viewsets.GenericViewSet):
    serializer_class = CharacterSerializer
    queryset = Character.objects.all()

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def become(self, request, pk):
        character = None
        try:
            character = Character.objects.get(user=request.user, pk=pk)
        except Character.DoesNotExist:
            raise GrottoGameWarning("Character doesn't exist")
        request.user.character = character
        request.user.save()
        request.character = character


class ItemViewSet(GameActionMixin, viewsets.GenericViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def generic_action(self, request, pk, action="test", holder="character"):
        item_service = ItemService()
        item = item_service.get_item(
            character=request.character, pk=pk, holder=holder)
        service_return = getattr(item_service, self.action)(
            item=item, character=request.character
        )
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)
        return Response("this should get overwritten!")

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def use(self, request, pk):
        return self.generic_action(request, pk, action="use")

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def place(self, request, pk):
        return self.generic_action(request, pk, action="place")

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def take(self, request, pk):
        return self.generic_action(request, pk, action="take", holder="room")

    @swagger_auto_schema(responses={200: serializers.TableauSerializer})
    @action(
        detail=True,
        methods=["post"],
        serializer_class=serializers.NullSerializer,
    )
    def drop(self, request, pk):
        return self.generic_action(request, pk, action="drop")
