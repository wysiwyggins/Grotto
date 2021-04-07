from random import choice

from characterBuilder.models import Visit
from mapBuilder.models import Room


class PlayerCharacterDeathService:
    def __init__(self, *, character, deathnote, **kwargs):
        character.dead = True
        character.deathnote = deathnote
        # remove character from the room
        Visit.objects.create(room=character.room, character=character, died_here=True)
        character.room = None
        character.save()


class NonPlayerCharacterMovementService:
    def __init__(self, *, npc, room="adjacent", **kwargs):
        # npc moves
        # choose a destination
        current = npc.room
        if room == "random":
            future = choice(Room.objects.all())
        elif isinstance(room, (Room,)):
            future = room
        else:
            future = choice(current.exits.all())
        npc.room = future
        npc.movement_entropy = 0
        npc.save()
        # does it kill?
        if npc.deadly:
            # kill any player characters in the room
            for unlucky in future.occupants.all():
                PlayerCharacterDeathService(
                    character=unlucky,
                    deathnote=f"{unlucky.name} was killed by {npc.name}",
                )


class NonPlayerCharacterDeathService:
    def __init__(self, *, npc, killer, **kwargs):
        # transfer loot to killer
        killer.items.add(*npc.loot.all())
        # npc is placed in random room
        NonPlayerCharacterMovementService(npc=npc, room="random")
