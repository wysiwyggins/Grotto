from random import choice, randint

from django.contrib import messages
from django.http import Http404
from django.views.generic import FormView, RedirectView, TemplateView

from characterBuilder.models import Character, NonPlayerCharacter, Visit
from Grotto.game.services import (
    NonPlayerCharacterService,
    PlayerCharacterService,
)
from mapBuilder.models import Room
from itemBuilder.models import Item
from itemBuilder.enum import ItemType
from Grotto.game.services import ItemService, GameService


class LivingCharacterBaseView(RedirectView):
    pattern_name = "mapBuilder:room"

    def dispatch(self, request, *args, **kwargs):
        if request.character is None:
            raise Http404("Character does not exist")
        # is this character alive
        if request.character.dead:
            # send the plater back to the grotto
            self.pattern_name = "characterBuilder:crypt"
            # message about death
            messages.add_message(request, messages.INFO, request.character.deathnote)
            return super().get(request)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, dice_count=1, **kwargs):
        # get current room
        colorSlug = kwargs.get("colorSlug")
        ItemService().burnable_swap()
        game = GameService()
        if colorSlug:
            try:
                room = Room.objects.get(colorSlug=colorSlug)
            except Room.DoesNotExist:
                pass
            else:
                game.roll_to_dirty_room(room=room, dice_count=dice_count)
        service_return = game.roll_to_move_npcs(dice_count=dice_count)

        # send messages
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)

        request.character.refresh_from_db()
        if request.character.dead:
            # send the plater back to the grotto
            self.pattern_name = "characterBuilder:crypt"
            return super().get(request)
        return super().get(request, *args, **kwargs)


class EnterGrottoView(LivingCharacterBaseView):
    def get(self, request, *args, **kwargs):
        if request.character.room is None:
            # choose a random, but safe room to enter
            request.character.room = Room.objects.exclude(
                npcs__deadly=True).order_by("?")[0]
            request.character.save()
            # redirect user to appropriate room
        kwargs.update({"colorSlug": request.character.room.colorSlug})
        return super().get(request, *args, **kwargs)


class MoveView(LivingCharacterBaseView):
    def get(self, request, *args, colorSlug, **kwargs):
        service_return = PlayerCharacterService().move(
            character=request.character, raises=Http404, colorSlug=colorSlug)
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)
        kwargs.update({"colorSlug": request.character.room.colorSlug, "dice_count": 1})
        return super().get(request, *args, **kwargs)


class FireArrowView(LivingCharacterBaseView):
    pattern_name = "mapBuilder:room"

    def get(self, request, *args, colorSlug, **kwargs):
        service_return = PlayerCharacterService().fire_arrow(
            character=request.character, colorSlug=colorSlug, raises=Http404)
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)
        kwargs.update({"colorSlug": request.character.room.colorSlug, "dice_count": 5})
        return super().get(request, *args, **kwargs)


class BecomeCharacterView(EnterGrottoView):
    pattern_name = "mapBuilder:room"

    def dispatch(self, request, *args, character_pk, **kwargs):
        character = None
        try:
            character = Character.objects.get(user=request.user, pk=character_pk)
        except Character.DoesNotExist:
            raise Http404("Character doesn't exist")
        request.user.character = character
        request.user.save()
        request.character = character
        return super().dispatch(request, *args, **kwargs)


class BaseItemActionView(LivingCharacterBaseView):
    action = "test"
    holder = "character"

    def get(self, request, *args, item_pk, **kwargs):
        item_service = ItemService()
        item = item_service.get_item(
            character=request.character, pk=item_pk, holder=self.holder, raises=Http404)
        service_return = getattr(item_service, self.action)(
            item=item, character=request.character)
        for message in service_return.messages:
            messages.add_message(request, messages.INFO, message)

        kwargs.update({"colorSlug": request.character.room.colorSlug, "dice_count": 1})
        return super().get(request, *args, **kwargs)


class UseItemView(BaseItemActionView):
    action = "use"


class PlaceItemView(BaseItemActionView):
    action = "place"


class TakeItemView(BaseItemActionView):
    action = "take"
    holder = "room"


class DropItemView(BaseItemActionView):
    action = "drop"


class ViewItemView(LivingCharacterBaseView):
    action = "view"
    holder = "room"
    pattern_name = "mapBuilder:cenotaph"

    def get(self, request, *args, item_pk, **kwargs):
        item = ItemService().get_item(
            character=request.character, pk=item_pk, holder=self.holder, raises=Http404)

        kwargs.update({"colorSlug": request.character.room.colorSlug, "dice_count": 1})
        return super().get(request, *args, **kwargs)
