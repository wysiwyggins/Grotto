import io
import random

from itemBuilder.enum import ItemType


class ItemGeneratorService:

    # Items! Player characters all start with a random item and an arrow. 
    # Items can be given to characters, put in rooms and taken from rooms, they cannot be taken from characters
    # Items also have an action function depending on their type
    # It's a bad (awesome) idea but they could also have a file attachment

    # some of these items suggest new room attributes too: lit, dirty and honored, these could be used for fun stuff
    # items like rooms could possibly be edited with a magic item taken from the wumpus (amulet?)

    # I added the "burn" action stub to junk since it would show how to eventually have actions that use up an item

    _item_types = {
        ItemType.JUNK: "generateJunk",
        ItemType.CANDLE: "generateCandle",
        ItemType.INCENSE: "generateIncense",
        ItemType.SCRUBBRUSH: "generateScrubBrush",
        ItemType.AMULET: "generateJunk",
        ItemType.ARROW: "generateArrow",
    }

    def generate(self, item_type, abstract_item_name):
        if item_type not in self._item_types:
            return "boring", "standard"
        return getattr(self, self._item_types[item_type])(name=abstract_item_name)

    def __init__(self, *, seed=None):
        self.seed = seed or random.randint(0, 999999)
        self.name = "Candle"
        self.description = "A wax candle"
        self.active = False #yeah I dunno about this, this is all pseudocode right now
        # could have file attachments too if we wanted to live really dangerously!

    def generateItem(self, *, user=None):
        random.seed(self.seed)
        itemType = random.randint(0, 4)
        if itemType <= 2:
            self.generateCandle()
        elif itemType == 3:
            self.generateIncense()
        elif itemType == 4:
            self.generateScrubBrush()
        else:
            self.generateJunk()

    def getItemName(self):
        itemFO = open("word_lists/items.txt")
        itemList = list(itemFO)
        selection = random.randint(0, len(itemList) - 1)
        item = itemList[selection]
        item = item.rstrip("\n")
        itemFO.close()
        return item

    def getColor(self):
        colorsFO = open("word_lists/colors.txt")
        colorsList = list(colorsFO)
        colorsSelection = random.randint(0, len(colorsList) - 1)
        color = colorsList[colorsSelection]
        color = color.rstrip("\n")
        colorsFO.close()
        return color
    
    def getSubstance(self):
        random.seed(self.seed)
        substanceFO = io.open(
            "word_lists/substances.txt", encoding="utf-8"
        )
        substanceList = list(substanceFO)
        selection = random.randint(0, len(substanceList) - 1)
        substance = substanceList[selection]
        substance = substance.rstrip("\n")
        return substance
    
    def getAdjective(self):
        adjectiveFO = open("word_lists/adjectives.txt")
        adjectiveList = list(adjectiveFO)
        selection = random.randint(0, len(adjectiveList) - 1)
        adjective = adjectiveList[selection]
        adjective = adjective.rstrip("\n")
        return adjective
    
    def generateCandle(self, name=None):
        color = self.getColor()
        name = "candle"
        self.item_name = name
        self.item_description = "a pure " + color + " wax " + name
        return self.item_name, self.item_description
    
    def generateIncense(self, name=None):
        color = self.getColor()
        substance = self.getSubstance()
        name = "incense"
        self.item_name = name
        self.item_description = substance + name
        return self.item_name, self.item_description
    
    def generateScrubBrush(self, name=None):
        color = self.getColor()
        name = "scrub brush"
        self.item_name = name
        self.item_description = color + name
        return self.item_name, self.item_description

    def generateJunk(self, name=None):
        color = self.getColor()
        substance = self.getSubstance()
        if "candle" not in name:
            name = self.getItemName()
        self.item_name = name
        self.item_description = name + " made of " + color + " " + substance
        return self.item_name, self.item_description

    def generateAmulet(self, name=None):
        color = self.getColor()
        substance = self.getSubstance()
        self.item_name = "Amulet"
        self.item_description = self.item_name + " made of " + color + " " + substance
        return self.item_name, self.item_description

    def generateArrow(self, name=None):
        color = self.getColor()
        substance = self.getSubstance()
        self.item_name = "Arrow"
        self.item_description = self.item_name + " made of " + color + " " + substance
        return self.item_name, self.item_description
