from random import choice, randint

from django.contrib import messages
from django.http import Http404
from django.views.generic import TemplateView, FormView, RedirectView

from characterBuilder.models import Character, Visit, NonPlayerCharacter
from mapBuilder.models import Room


class LivingCharacterBaseView(RedirectView):
    pattern_name = "mapBuilder:room"

    def dispatch(self, request, *args, **kwargs):
        if request.character is None:
            raise Http404("Character does not exist")
        # is this character alive
        if request.character.dead:
            # send the plater back to the grotto
            self.pattern_name = "characterBuilder:index"
            # message about death
            messages.add_message(
                request, messages.INFO, request.character.deathnote)
            return super().get(request)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, *, dice_count=1, **kwargs):
        for npc in NonPlayerCharacter.objects.filter(mobile=True):
            entropy = 0
            # roll appropriate number of dice
            for x in range(dice_count):
                entropy += randint(1, 20)
            # add the quantity to the entropy score for every mobile NPC
            npc.movement_entropy += entropy
            # resolve any NPC movements
            if npc.movement_threshold <= npc.movement_entropy:
                # TODO: npc does move!
                npc.movement_entropy = 0
                pass
            npc.save()
        return super().get(request, *args, **kwargs)


class EnterGrottoView(LivingCharacterBaseView):
    pattern_name = "mapBuilder:room"

    def get(self, request, *args, **kwargs):
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


class MoveView(LivingCharacterBaseView):
    pattern_name = "mapBuilder:room"

    def get(self, request, *args, **kwargs):
        if request.character.room is None:
            raise Http404("Character is not in Grotto")
        old_room = request.character.room
        try:
            room = old_room.exits.get(colorSlug=kwargs.get("colorSlug"))
        except Room.DoesNotExist:
            raise Http404("Room is not accessable")
        # pick up any arrows in the room
        arrow_count = room.arrow_count
        if arrow_count > 0:
            # message user about the arrows they picked up
            room.arrow_count = 0
            room.save()
            messages.add_message(
                request, messages.INFO, f'You have picked up arrows ({arrow_count})')
            request.character.arrow_count += arrow_count
        request.character.room = room
        request.character.save()
        Visit.objects.create(room=old_room, character=request.character)
        return super().get(request, colorSlug=request.character.room.colorSlug)


class FireArrowView(LivingCharacterBaseView):
    pattern_name = "mapBuilder:room"

    def get(self, request, *args, **kwargs):
        character = request.character
        if character.room is None:
            raise Http404("Character is not in Grotto")
        # check that the room being fired into is adjancent to character room
        try:
            target_room = character.room.exits.get(colorSlug=kwargs.get("colorSlug"))
        except Room.DoesNotExist:
            raise Http404("Room is not accessable")
        # check that character has an arrow
        if character.arrow_count < 0:
            raise Http404("You don't have any arrows")
        character.arrow_count -= 1
        character.save()
        # see what is in room (wumpus or player character or nothing)
        occupants = list(target_room.occupants.all())
        if occupants:
            unlucky = choice(occupants)
            # kill unlucky
            unlucky.dead = True
            unlucky.deathnote = f"{character.name} was killed by an arrow from the {character.room}"
            # remove unlucky from the room
            Visit.objects.create(room=unlucky.room, character=unlucky, died_here=True)
            unlucky.room = None
            unlucky.save()
        else:
            target_room.arrow_count += 1
            target_room.save()
        return super().get(
            request,
            colorSlug=character.room.colorSlug,
            dice_count=5)
