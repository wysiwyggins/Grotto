from random import choice

from django.http import Http404
from django.views.generic import TemplateView, FormView, RedirectView

from characterBuilder.models import Character, Visit
from mapBuilder.models import Room


class EnterGrottoView(RedirectView):
    pattern_name = "mapBuilder:room"

    def get(self, request, *args, **kwargs):
        # is this an actual character
        if request.character is None:
            raise Http404("Character does not exist")
        # is the character already in the map
        if request.character.room is None:
            # choose a random room to enter
            pks =  Room.objects.values_list('id', flat=True).order_by('id')
            random_pk = choice(pks)
            room = Room.objects.get(id=random_pk)
            # send character there
            request.character.room = room
            request.character.save()
            # redirect user to appropriate room
        return super().get(request, colorSlug=request.character.room.colorSlug)


class MoveView(RedirectView):
    pattern_name = "mapBuilder:room"

    def get(self, request, *args, **kwargs):
        # is this an actual character
        if request.character is None:
            raise Http404("Character does not exist")
        if request.character.room is None:
            raise Http404("Character is not in Grotto")
        old_room = request.character.room
        try:
            room = old_room.exits.get(colorSlug=kwargs.get("colorSlug"))
        except Room.DoesNotExist:
            raise Http404("Room is not accessable")
        request.character.room = room
        request.character.save()
        Visit.objects.create(room=old_room, character=request.character)
        return super().get(request, colorSlug=request.character.room.colorSlug)
