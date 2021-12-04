from random import choice, randint

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
        if npc.demonic:
            npc.room.is_cursed = True
            npc.room.save()
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


class RandomColorService:
    def get_elaborate_color(self):
        with open("word_lists/colors.txt") as f:
            colors = f.readlines()
        # colorFO = io.open("word_lists/colors.txt", encoding="utf-8")
        # colors = list(colorFO)
        # selection = randint(0, len(colors) - 1)
        elaborate_color = choice(colors).rstrip("\n")
        return elaborate_color

    def get_color(self):
        elaborate_color = self.get_elaborate_color()
        red = randint(0, 255)
        green = randint(0, 255)
        blue = randint(0, 255)
        color = []
        if "red" in elaborate_color:
            red = randint(100, 255)
        if "green" in elaborate_color:
            green = randint(100, 255)
            red -= randint(100, 255)
            blue -= randint(100, 255)
        if "blue" in elaborate_color:
            blue = randint(100, 255)
            red -= randint(100, 255)
            green -= randint(100, 255)
        if "violet" in elaborate_color:
            blue = randint(100, 255)
            red = randint(100, 255)
            green -= randint(100, 255)
        if "orange" in elaborate_color:
            green = randint(100, 255)
            red = randint(200, 255)
            blue -= randint(100, 255)
        if "tangerine" in elaborate_color:
            green = randint(100, 255)
            red = randint(200, 255)
            blue -= randint(100, 255)
        if "yellow" in elaborate_color:
            green = randint(200, 255)
            red = randint(200, 255)
            blue -= randint(100, 255)
        if "gold" in elaborate_color:
            green = randint(220, 255)
            red = randint(220, 255)
            blue =randint(0, 20)
        if "cyan" in elaborate_color:
            red -= randint(100, 255)
            green = randint(200, 255)
            blue = randint(200, 255)
        if "aqua" in elaborate_color:
            red = 0
            green = randint(200, 255)
            blue = randint(200, 255)
        if "azure" in elaborate_color:
            blue = randint(200, 255)
            red = 0
        if "brown" in elaborate_color:
            red = randint(200, 255)
            green = 75
            blue = 0
        if "chocolate" in elaborate_color:
            red = randint(200, 255)
            green = 75
            blue = 0
        if "pink" in elaborate_color:
            red = 255
            green = randint(100, 200)
            blue = randint(100, 200)
        if "salmon" in elaborate_color:
            red = 255
            green = randint(100, 200)
            blue = randint(100, 200)
        if "coral" in elaborate_color:
            red = 255
            green = randint(100, 200)
            blue = randint(50, 100)
        if "crimson" in elaborate_color:
            red = randint(200, 255)
            blue = 38
            green = 54
        if "fuchsia" in elaborate_color:
            red = 145
            blue = 92
            green = 131
        if "gray" in elaborate_color:
            red = 100
            green = 100
            blue = 100
        if "black" in elaborate_color:
            if(red>0):
                red -= 200
            if(green>0):
                green -= 200
            if(blue>0):
                blue -= 200
        if "white" in elaborate_color:
            if(red<255):
                red += 200
            if(green<255):
                green += 200
            if(blue<255):
                blue += 200

        #oh god I don't know how to clamp in python
        if(red > 255):
            red = 255
        if(green > 255):
            green = 255
        if(blue > 255):
            blue = 255
        if(red < 0):
            red = 0
        if(green < 0):
            green = 0
        if(blue < 0):
            blue = 0
        color.append(red)
        color.append(green)
        color.append(blue)
        return elaborate_color, color