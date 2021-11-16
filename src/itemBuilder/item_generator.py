import io
import random
from django.utils.text import slugify

from characterBuilder import models


class Item(DefaultObject):

    # Items! Player characters all start with a random item and an arrow. 
    # Items can be given to characters, put in rooms and taken from rooms, they cannot be taken from characters
    # Items also have an action function depending on their type
    # It's a bad (awesome) idea but they could also have a file attachment

    # some of these items suggest new room attributes too: lit, dirty and honored, these could be used for fun stuff
    # items like rooms could possibly be edited with a magic item taken from the wumpus (amulet?)

    # I added the burn action to junk since it would show how to eventually have actions that use up an item

    def lightCandle(self):
        self.active = True
        # light candle action
        # this sets the candle to lit, putting a lit candle in a room changes the room's light value
        # rooms can be dim, lit or dark. Dark rooms can't be traversed at all, you could be eaten by a wumpus
        # carrying a lit candle makes whatever room you are in dim, placing a lit candle in a room makes the room lit
    
    def lightIncense(self):
        self.active = True
        # A room can be honored or neglected, placing lit incense in the room makes the room honored
    
    def useScrubBrush(self):
        self.active = True
        # A room can be clean, dirty or profane. Using a Scrub brush in a room cleans it. 
        # When a room is clean it has an inscription that appears with the name and dates of the deceased
        # when a room is profane ???
    
    def burnJunk(self):
        self.active = True
        # maybe the default action of junk is to burn it

    def __init__(self, *, seed=None):
        self.seed = seed or random.randint(0, 999999)
        self.name = "Candle"
        self.action = Item().lightCandle
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
        itemFO = open("/word_lists/items.txt")
        itemList = list(itemFO)
        selection = random.randint(0, len(itemList) - 1)
        item = itemList[selection]
        item = item.rstrip("\n")
        itemFO.close()
        return item

    def getColor(self):
        colorsFO = open("/word_lists/colors.txt")
        colorsList = list(colorsFO)
        colorsSelection = random.randint(0, len(colorsList) - 1)
        color = colorsList[colorsSelection]
        color = color.rstrip("\n")
        colorsFO.close()
        return color
    
    def getSubstance(self):
        random.seed(self.seed)
        substanceFO = io.open(
            f"{self.base_dir}word_lists/substances.txt", encoding="utf-8"
        )
        substanceList = list(substanceFO)
        selection = random.randint(0, len(substanceList) - 1)
        substance = substanceList[selection]
        substance = substance.rstrip("\n")
        return substance
    
    def getAdjective(self):
        adjectiveFO = open("typeclasses/itemator/word_lists/adjectives.txt")
        adjectiveList = list(adjectiveFO)
        selection = random.randint(0, len(adjectiveList) - 1)
        adjective = adjectiveList[selection]
        adjective = adjective.rstrip("\n")
        return adjective
    
    def generateCandle(self):
        color = self.getColor()
        name = "candle"
        self.item_name = name
        self.item_description = "a pure " + color + " wax " + name
        self.action = Item().lightCandle
        return self.createModelInstance()
    
    def generateIncense(self):
        color = self.getColor()
        substance = self.getSubstance()
        name = "incense"
        self.item_name = name
        self.item_description = substance + name
        self.action = Item().lightIncense
        return self.createModelInstance()
    
    def generateScrubBrush(self):
        color = self.getColor()
        name = "scrub brush"
        self.item_name = name
        self.item_description = color + name
        self.action = Item().useScrubBrush
        return self.createModelInstance()

    def generateJunk(self):
        color = self.getColor()
        substance = self.getSubstance()
        adjective = self.getAdjective()
        name = self.getItemName()
        self.item_name = name
        anAdjective = self.addAorAn(adjective)
        self.item_description = anAdjective + " " + \
            name + " made of " + color + " " + substance + "."
        self.action = Item().burnJunk
        return self.createModelInstance()