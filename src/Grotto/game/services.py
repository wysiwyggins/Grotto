from datetime import timedelta
from random import choice, randint

from django.utils.timezone import now
from django.db.models import F

from characterBuilder.models import Visit
from mapBuilder.models import Room
from itemBuilder.models import Item, AbstractItem, Swap
from itemBuilder.enum import ItemType
from itemBuilder.item_generator import ItemGeneratorService


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
        if current is None:
            room = "random"
        future = None
        if room == "random":
            all_rooms = Room.objects.all()
            dank_rooms = []
            for room in all_rooms:
                attributes = room.get_attributes()
                if attributes["brightness"] == 0 and attributes["sanctity"] == 0:
                    dank_rooms.append(room)
            if dank_rooms:
                future = choice(dank_rooms)
        elif isinstance(room, (Room,)):
            future = room
        else:
            future = choice(current.exits.all())
        npc.room = future
        npc.movement_entropy = 0
        npc.save()
        if npc.demonic and npc.room:
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
            blue = randint(0, 20)
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
            if red > 0:
                red -= 200
            if green > 0:
                green -= 200
            if blue > 0:
                blue -= 200
        if "white" in elaborate_color:
            if red < 255:
                red += 200
            if green < 255:
                green += 200
            if blue < 255:
                blue += 200

        # oh god I don't know how to clamp in python
        if red > 255:
            red = 255
        if green > 255:
            green = 255
        if blue > 255:
            blue = 255
        if red < 0:
            red = 0
        if green < 0:
            green = 0
        if blue < 0:
            blue = 0
        color.append(red)
        color.append(green)
        color.append(blue)
        return elaborate_color, color


class ItemServiceReturn:
    def __init__(self, *, messages=None):
        self.messages = messages or []


# service
class ItemService:
    def create(self, *, abstract_item, character=None, room=None):
        color_name, color_hex = RandomColorService().get_color()
        item_name, item_description = ItemGeneratorService().generate(
            item_type=abstract_item.itemType,
            abstract_item_name=abstract_item.itemName,
        )
        return Item.objects.create(
            name=item_name,
            description=item_description,
            abstract_item=abstract_item,
            current_owner=character,
            current_room=room,
            colorName=color_name,
            colorHex=color_hex,
        )

    def use(self, *, item, character):  # Item model instance
        # validate that the item type exists
        ret = ItemServiceReturn()
        if item.abstract_item.itemType == ItemType.CANDLE:
            self._use_burnable(item, character)
        if item.abstract_item.itemType == ItemType.INCENSE:
            self._use_burnable(item, character)
            self.place(item, character)
        if item.abstract_item.itemType == ItemType.SCRUBBRUSH:
            self._use_scrubbrush(item, character)
        if item.abstract_item.itemType == ItemType.JUNK:
            ret.messages.append("You're not sure how to use this")
        if item.abstract_item.itemType == ItemType.ARROW:
            ret.messages.append("That's not how you use this")
        return ret

    def place(self, item, character):
        ret = ItemServiceReturn()
        item.current_owner = None
        item.current_room = character.room
        item.save()
        if item.abstract_item.itemType == ItemType.INCENSE and item.is_active:
            character.room.is_cursed = False
            character.room.save()
        return ret

    def take(self, item, character):
        ret = ItemServiceReturn()
        if item.is_active and item.abstract_item.untakable_if_active:
            # cannot pick up an active candle
            ret.messages.append("Cannot be taken when active")
        elif item.abstract_item.untakable:
            # cannot pick up a cenotaph
            ret.messages.append("Cannot be taken")
        else:
            item.current_owner = character
            item.current_room = None
            item.save()
            ret.messages.append(f"you picked {item.abstract_item.itemName} up")
        return ret

    def drop(self, item, character):
        # actually drop item
        item.current_owner = None
        item.current_room = character.room
        item.save()
        ret = ItemServiceReturn()
        print("dropping item")
        self.check_swap(character.room, return_obj=ret)
        return ret

    def check_swap(self, room, *, return_obj=None):
        # check for anyone who wants item in room and drop resulting item
        for swap in Swap.objects.filter(npc__in=room.npcs.all()):
            for item in room.items.filter(abstract_item__itemType=swap.picks_type):
                if return_obj is not None:
                    return_obj.messages.append(swap.message)
                self.create(abstract_item=swap.puts, room=room)
                self.destroy(item)

    def burnable_swap(self):
        """Check the room for burned out candles and replace them with a junk item"""
        abstract_spent_candle, _ = AbstractItem.objects.get_or_create(
            itemType=ItemType.JUNK,
            itemName="Spent Candle",
            itemDescription="A little fleck of wick sits at the bottom",
        )
        for old_candle in Item.objects.exclude(
            abstract_item__active_time__isnull=True,
            active__isnull=True,
        ).filter(
            abstract_item__itemType=ItemType.CANDLE,
            active__lte=now()-F("abstract_item__active_time"),
        ):
            self.create(
                abstract_item=abstract_spent_candle,
                room=old_candle.current_room,
                character=old_candle.current_owner,
            )
            old_candle.delete()


    def destroy(self, item):
        item.current_room = None
        item.current_owner = None
        item.save()

    def _use_burnable(self, item, character):
        if item.active:
            return
        item.active = now()
        item.save()

    def _use_scrubbrush(self, item, character):
        room = character.room
        room.cleanliness = min(2, room.cleanliness + 1)
        room.save()

    def _use_incense(self, item, character):
        pass

    def _use_amulet(self, item, character):
        pass


class NonPlayerCharacterDeathService:
    def __init__(self, *, npc, killer, **kwargs):
        # transfer loot to room
        [
            ItemService().create(abstract_item=a_i, room=npc.room)
            for a_i in npc.loot.all()
        ]
        # npc is placed in random room
        NonPlayerCharacterMovementService(npc=npc, room="random")
