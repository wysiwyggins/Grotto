import markovify
import spacy
import re
import io
import random
import webcolors
from unidecode import unidecode
from hashids import Hashids
from mapBuilder.models import Room
from mapBuilder.services import RoomAdjacencyService


def generateRoom():
    hashids = Hashids()
    title = " "
    roomDescription = " "
    index = 0
    codexList = []

    nlp = spacy.load("en_core_web_sm")
    # since I moved this script to django it's not finding its txt files. I tried putting them in static too
    with open("mapBuilder/corpuses/rooms.txt") as f:
        text = f.read()

    text_model = markovify.Text(text)
    text_model = text_model.compile()

    class POSifiedText(markovify.Text):
        def word_split(self, sentence):
            return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

        def word_join(self, words):
            sentence = " ".join(word.split("::")[0] for word in words)
            return sentence

    def getElaborateColor():
        colorFO = io.open("mapBuilder/word_lists/colors.txt", encoding="utf-8")
        colorList = list(colorFO)
        selection = random.randint(0, len(colorList) - 1)
        elaborateColor = colorList[selection]
        elaborateColor = elaborateColor.rstrip("\n")
        return elaborateColor

    def getColor(elaborateColor):
        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        color = []
        if "red" in elaborateColor:
            red = random.randint(100, 255)
        if "green" in elaborateColor:
            green = random.randint(100, 255)
            red -= random.randint(100, 255)
            blue -= random.randint(100, 255)
        if "blue" in elaborateColor:
            blue = random.randint(100, 255)
            red -= random.randint(100, 255)
            green -= random.randint(100, 255)
        if "violet" in elaborateColor:
            blue = random.randint(100, 255)
            red = random.randint(100, 255)
            green -= random.randint(100, 255)
        if "orange" in elaborateColor:
            green = random.randint(100, 255)
            red = random.randint(200, 255)
            blue -= random.randint(100, 255)
        if "tangerine" in elaborateColor:
            green = random.randint(100, 255)
            red = random.randint(200, 255)
            blue -= random.randint(100, 255)
        if "yellow" in elaborateColor:
            green = random.randint(200, 255)
            red = random.randint(200, 255)
            blue -= random.randint(100, 255)
        if "gold" in elaborateColor:
            green = random.randint(220, 255)
            red = green + random.randint(10, 20)
            blue =random.randint(0, 20)
        if "cyan" in elaborateColor:
            red -= random.randint(100, 255)
            green = random.randint(200, 255)
            blue = random.randint(200, 255)
        if "aqua" in elaborateColor:
            red = 0
            green = random.randint(200, 255)
            blue = random.randint(200, 255)
        if "turquoise" in elaborateColor:
            red=64
            green=224
            blue=204
        if "azure" in elaborateColor:
            blue = random.randint(200, 255)
            red = 0
        if "brown" in elaborateColor:
            red = random.randint(200, 255)
            green = 75
            blue = 0
        if "chocolate" in elaborateColor:
            red = random.randint(200, 255)
            green = 75
            blue = 0
        if "pink" in elaborateColor:
            red = 255
            green = random.randint(100, 200)
            blue = green
        if "coral" in elaborateColor:
            red = 255
            green = random.randint(100, 200)
            blue = random.randint(50, 100)
        if "crimson" in elaborateColor:
            red = random.randint(200, 255)
            blue = 38
            green = 54
        if "fuchsia" in elaborateColor:
            red = 145
            blue = 92
            green = 131
        if "gray" in elaborateColor:
            red = 100
            green = 100
            blue = 100
        if "grey" in elaborateColor:
            red = 100
            green = 100
            blue = 100
        if "black" in elaborateColor:
            if(red>0):
                red -= 200
            if(green>0):
                green -= 200
            if(blue>0):
                blue -= 200
        if "white" in elaborateColor:
            if(red<255):
                red += 200
            if(green<255):
                green += 200
            if(blue<255):
                blue += 200
        if "hot" in elaborateColor:
            red = 255
        if "cold" in elaborateColor:
            blue = 255

        red = max(min(red, 255), 0)
        green = max(min(green, 255), 0)
        blue = max(min(blue, 255), 0)
        color.append(red)
        color.append(green)
        color.append(blue)
        return color

    print("generating...")

    elaborateColor = getElaborateColor()
    colorhex= webcolors.rgb_to_hex(getColor(elaborateColor))
    try:
        title = text_model.make_short_sentence(60)
        title = title[:-1]
    except:
        title = text_model.make_short_sentence(120)
    hashids = Hashids(salt=title)
    # myfile = "rooms/room-"+str(i)+id+".html"
    #with open(myfile, "a") as myfile:
    #    myfile.write("<html><head><meta charset='UTF-8'><link rel='stylesheet' href='stylesheet.css' type='text/css' media='screen' charset='utf-8'> <title>"+elaborateColor+" room</title></head>")
    #    myfile.write("<body style='background-color:"+colorhex+";'>")
    #    myfile.write("<section class='description'><h1>"+elaborateColor+" room</h1> <p>")
    for number in range(5):
        roomDescription += "\n" + text_model.make_sentence() + " "

    #    myfile.close()

        # new version

    room = Room.objects.create( name = elaborateColor.capitalize() + " Room", description = roomDescription, colorHex = colorhex, colorName = elaborateColor)
    RoomAdjacencyService().add_room(room)
