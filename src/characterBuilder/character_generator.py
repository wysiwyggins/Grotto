import io
import random

import markovify
from django.utils.text import slugify

from characterBuilder import models


# in the pre-pyglet version you were able to type in a seed number and consistently get the same output from the same seed.
class Character:
    base_dir = "characterBuilder/"

    def __init__(self, *, seed=None):
        self.seed = seed or random.randint(0, 999999)
        self.name = "Wiley Wiggins"
        self.kind = "Human"
        self.description = "A middle-aged, pasty art student"
        self.skills = {"procrastination": 12, "irritability": 18}

    def generateCharacter(self, *, user=None):
        random.seed(self.seed)
        characterType = random.randint(0, 9)
        if characterType <= 2:
            self.generateHuman()
        elif characterType == 3:
            self.generateFungus()
        elif characterType == 4:
            self.generateVegetable()
        elif characterType == 5:
            self.generateAnimal()
        elif characterType == 6:
            self.generateBird()
        elif characterType == 7:
            self.generateObelisk()
        elif characterType == 8:
            self.generateGhost()
        else:
            self.generateRobot()

        return self.createModelInstance(user=user)

    def createModelInstance(self, *, user):
        character = models.Character.objects.create(
            name=self.name,
            kind=self.kind,
            description=self.description,
            user=user,
        )
        for skill, level in self.skills.items():
            models.Skill.objects.create(
                name=skill,
                level=level,
                character=character,
            )
        return character

    def getSkills(self):
        random.seed(self.seed)
        skillsFO = io.open(f"{self.base_dir}word_lists/skills.txt", encoding="utf-8")
        skillsList = list(skillsFO)
        skillsFO.close()
        skills = {}
        for n in range(4):
            selection = random.randint(0, len(skillsList) - 1)
            skill = skillsList[selection]
            skill = skill.rstrip("\n")
            skills[skill] = random.randint(-10, 18)
        return skills

    # substances and adjectives will be shared by multiple character types

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

    def getAdjective(self, reversed):
        random.seed(self.seed)
        adjectiveFO = io.open(
            f"{self.base_dir}word_lists/adjectives.txt", encoding="utf-8"
        )
        adjectiveList = list(adjectiveFO)
        selection = random.randint(0, len(adjectiveList) - 1)

        # This lets us pick from two different random names with the same seed, for two adjectives in one character.

        if reversed == True:
            adjective = adjectiveList[-selection]
        else:
            adjective = adjectiveList[selection]
        adjective = adjective.rstrip("\n")
        return adjective

    # here's the functions to make a human

    def generateHumanName(self):
        random.seed(self.seed)
        # pick a first name
        firstnameFO = io.open(
            f"{self.base_dir}word_lists/firstnames.txt", encoding="utf-8"
        )
        firstnameList = list(firstnameFO)
        selection = random.randint(0, len(firstnameList) - 1)
        firstname = firstnameList[selection]
        firstname = firstname.rstrip("\n")
        firstnameFO.close()

        # pick a last name
        lastnameFO = io.open(
            f"{self.base_dir}word_lists/lastnameBeginnings.txt", encoding="utf-8"
        )
        lastnameEndingsFO = io.open(
            f"{self.base_dir}word_lists/lastnameEndings.txt", encoding="utf-8"
        )
        lastnameList = list(lastnameFO)
        lastnameEndingsList = list(lastnameEndingsFO)
        selection = random.randint(0, len(lastnameList) - 1)
        lastname = lastnameList[selection]
        lastname = lastname.rstrip("\n")
        selection = random.randint(0, len(lastnameEndingsList) - 1)
        lastnameEnding = lastnameEndingsList[selection]
        lastnameEnding = lastnameEnding.rstrip("\n")
        lastname = lastname + lastnameEnding
        name = firstname + " " + lastname
        return name
        lastnameFO.close()

    def getColor(self):
        random.seed(self.seed)
        colorsFO = io.open(f"{self.base_dir}word_lists/colors.txt", encoding="utf-8")
        colorsList = list(colorsFO)
        colorsSelection = random.randint(0, len(colorsList) - 1)
        color = colorsList[colorsSelection]
        color = color.rstrip("\n")
        colorsFO.close()
        return color

    def getClothing(self):
        random.seed(self.seed)
        clothesFO = io.open(f"{self.base_dir}word_lists/clothes.txt", encoding="utf-8")
        clothesList = list(clothesFO)
        color = self.getColor()
        clothesSelection = random.randint(0, len(clothesList) - 1)
        clothingItem = clothesList[clothesSelection]
        clothingItem = clothingItem.rstrip("\n")
        clothingItem = color + " " + clothingItem
        clothingItem = self.addAorAn(clothingItem)
        return clothingItem
        clothesFO.close()

    def getHair(self):
        random.seed(self.seed)
        hairFO = io.open(f"{self.base_dir}word_lists/hair.txt", encoding="utf-8")
        hairList = list(hairFO)
        selection = random.randint(0, len(hairList) - 1)
        hair = hairList[selection]
        hair = hair.rstrip("\n")
        hairFO.close()
        return hair

    def getCareer(self):
        random.seed(self.seed)
        careerFO = io.open(f"{self.base_dir}word_lists/careers.txt", encoding="utf-8")
        careerList = list(careerFO)
        selection = random.randint(0, len(careerList) - 1)
        career = careerList[selection]
        career = career.rstrip("\n")
        careerFO.close()
        return career

    def getItem(self):
        random.seed(self.seed)
        itemFO = io.open(f"{self.base_dir}word_lists/items.txt", encoding="utf-8")
        itemList = list(itemFO)
        selection = random.randint(0, len(itemList) - 1)
        item = itemList[selection]
        item = item.rstrip("\n")
        itemFO.close()
        return item

    def generateHuman(self):
        random.seed(self.seed)
        humanName = self.generateHumanName()
        clothingItem = self.getClothing()
        hairStyle = self.getHair()
        clothes = self.getClothing()
        adjective = self.getAdjective(False)
        career = self.getCareer()
        career = self.addAorAn(career)
        obeliskSubstance = self.getSubstance()
        petName = self.getAnimalName()
        petType = self.getAnimalType()
        petAdjective = self.getAdjective(True)
        item = self.getItem()
        item = self.addAorAn(item)
        self.kind = "Human"
        self.name = humanName
        self.description = (
            "A bipedal mammal with smooth skin and "
            + hairStyle
            + " hair on its head. It is wearing "
            + clothingItem
            + ". "
            + humanName
            + " worked as "
            + career
            + " before embarking on their "
            + adjective
            + " quest to find the legendary "
            + obeliskSubstance
            + " obelisk."
            + " They are followed by their faithful companion "
            + petName
            + " the "
            + petAdjective
            + " "
            + petType
            + ". "
        )
        self.skills = self.getSkills()
        self.items = self.getItem()

    # here's the animal functions
    def getAnimalName(self):
        random.seed(self.seed)
        # pick a first name
        nameFO = io.open(f"{self.base_dir}word_lists/firstnames.txt", encoding="utf-8")
        nameList = list(nameFO)
        selection = random.randint(0, len(nameList) - 1)
        name = nameList[
            -selection
        ]  # This is so animals have different names than humans even with the same seed
        name = name.rstrip("\n")
        nameFO.close()
        return name

    def generateAnimalDescription(self):
        animalDescription = " "
        random.seed(self.seed)
        animalCorpusFO = io.open(
            f"{self.base_dir}text_corpus/animal_corpus.txt", encoding="utf-8"
        )
        text = animalCorpusFO.read()
        text_model = markovify.NewlineText(text)
        try:
            animalDescription += text_model.make_short_sentence(140, tries=100) + " "
            animalDescription += text_model.make_sentence(tries=100) + " "
            animalDescription += text_model.make_sentence(tries=100) + " "
        except TypeError:
            animalDescription += "It hunts daily for food. "
        animalCorpusFO.close()
        return animalDescription

    def getAnimalType(self):
        animalTypeFO = io.open(
            f"{self.base_dir}word_lists/animals.txt", encoding="utf-8"
        )
        animalList = list(animalTypeFO)
        selection = random.randint(0, len(animalList) - 1)
        animalType = animalList[selection]
        animalType = animalType.rstrip("\n")
        return animalType
        animalTypeFO.close()

    def generateAnimal(self):
        random.seed(self.seed)
        animalName = self.getAnimalName()
        animalType = self.getAnimalType()
        adjective = self.getAdjective(False)
        description = self.generateAnimalDescription()
        animalType = adjective + " " + animalType
        animalType = self.addAorAn(animalType)
        animalType = animalType.capitalize()
        self.kind = "Animal"
        self.name = animalName
        self.description = animalType + ". " + description
        self.skills = self.getSkills()

    # here's the bird functions

    def getBirdName(self):
        random.seed(self.seed)
        # pick a first name
        nameFO = io.open(f"{self.base_dir}word_lists/birdName.txt", encoding="utf-8")
        nameList = list(nameFO)
        selection = random.randint(0, len(nameList) - 1)
        name = nameList[selection]
        name = name.rstrip("\n")
        nameFO.close()
        return name

    def generateBirdDescription(self):
        random.seed(self.seed)
        birdDescription = " "
        birdCorpusFO = io.open(
            f"{self.base_dir}text_corpus/bird_corpus.txt", encoding="utf-8"
        )
        text = birdCorpusFO.read()
        text_model = markovify.NewlineText(text)
        for i in range(3):
            birdDescription += text_model.make_sentence(tries=100) + " "
        birdCorpusFO.close()
        return birdDescription

    def generateBird(self):
        random.seed(self.seed)
        name = self.getBirdName()
        enemyname = self.getAnimalName()
        enemyType = self.getAnimalType()
        adjective = self.getAdjective(False)
        adjective = self.addAorAn(adjective)
        description = self.generateBirdDescription()
        description = (
            description
            + " "
            + name
            + " the bird is hunted through life by its enemy, "
            + enemyname
            + ", "
            + adjective
            + " "
            + enemyType
            + "."
        )
        self.kind = "Bird"
        self.name = name
        self.description = description
        self.skills = self.getSkills()

    # veggies
    def generateVegetableDescription(self):
        random.seed(self.seed)
        vegetableDescription = " "
        veggieCorpusFO = io.open(
            f"{self.base_dir}text_corpus/veggie_corpus.txt", encoding="utf-8"
        )
        text = veggieCorpusFO.read()
        text_model = markovify.NewlineText(text)
        for i in range(2):
            vegetableDescription += text_model.make_sentence(tries=100) + " "
        veggieCorpusFO.close()
        return vegetableDescription

    def generateVegetable(self):
        random.seed(self.seed)
        veggieType = random.randint(1, 2)
        color = self.getColor()
        vegetableDescription = self.generateVegetableDescription()
        if veggieType == 1:
            pumpkinsFO = io.open(
                f"{self.base_dir}word_lists/pumpkins.txt", encoding="utf-8"
            )
            pumpkinsList = list(pumpkinsFO)
            selection = random.randint(0, len(pumpkinsList) - 1)
            veggieType = pumpkinsList[selection]
            veggieType = veggieType.rstrip("\n")
            pumpkinsFO.close()
        else:
            vegetablesFO = io.open(
                f"{self.base_dir}word_lists/vegetables.txt", encoding="utf-8"
            )
            vegetablesList = list(vegetablesFO)
            selection = random.randint(0, len(vegetablesList))
            veggieType = vegetablesList[selection]
            veggieType = veggieType.rstrip("\n")
            vegetablesFO.close()

        self.name = "nameless vegetable"
        self.kind = "Vegetable"
        color = self.addAorAn(color)
        self.description = color + " " + veggieType + ". " + vegetableDescription
        self.skills = {}

    # robot functions

    def getRobotName(self):
        random.seed(self.seed)
        # pick a first name
        nameFO = io.open(f"{self.base_dir}word_lists/robotName.txt", encoding="utf-8")
        nameList = list(nameFO)
        selection = random.randint(0, len(nameList) - 1)
        name = nameList[selection]
        name = name.rstrip("\n")
        name = name + "-" + str(random.randint(100, 1000))
        nameFO.close()
        return name

    def generateRobotDescription(self):
        random.seed(self.seed)
        robotDescription = " "
        robotCorpusFO = io.open(
            f"{self.base_dir}text_corpus/robot_corpus.txt", encoding="utf-8"
        )
        text = robotCorpusFO.read()
        text_model = markovify.Text(text)
        for i in range(4):
            robotDescription += text_model.make_sentence(tries=100) + " "
        robotCorpusFO.close()
        return robotDescription

    def generateRobot(self):
        name = self.getRobotName()
        description = self.generateRobotDescription()
        self.kind = "Robot"
        self.name = name
        self.description = "A hard working robot." + " " + description
        self.skills = self.getSkills()

    # fungus functions

    def generateFungiName(self):
        random.seed(self.seed)
        # pick a first name
        nameFO = io.open(f"{self.base_dir}word_lists/fungiName.txt", encoding="utf-8")
        nameList = list(nameFO)
        selection = random.randint(0, len(nameList) - 1)
        name = nameList[selection]
        name = name.rstrip("\n")
        nameFO.close()
        return name

    def generateFungus(self):
        random.seed(self.seed)
        fungiName = self.generateFungiName()
        nameFO = io.open(f"{self.base_dir}word_lists/fungiType.txt", encoding="utf-8")
        nameList = list(nameFO)
        selection = random.randint(0, len(nameList) - 1)
        fungiType = nameList[selection]
        fungiType = fungiType.rstrip("\n")
        adjective = self.getAdjective(False)
        color = self.getColor()
        self.kind = "Fungus"
        self.name = fungiName
        self.description = (
            "A colony of " + adjective + ", " + color + " " + fungiType + "."
        )
        self.skills = {}

    # ghost functions

    def getGhostName(self):
        random.seed(self.seed)
        # pick a first name
        nameFO = io.open(f"{self.base_dir}word_lists/ghostType.txt", encoding="utf-8")
        nameList = list(nameFO)
        selection = random.randint(0, len(nameList) - 1)
        name = nameList[selection]
        name = name.rstrip("\n")
        nameFO.close()
        return name

    def generateGhostDescription(self):
        random.seed(self.seed)
        adjective = self.getAdjective(False)
        adjective = self.addAorAn(adjective)
        ghostDescription = " "
        ghostCorpusFO = io.open(
            f"{self.base_dir}text_corpus/ghost_corpus.txt", encoding="utf-8"
        )
        text = ghostCorpusFO.read()
        text_model = markovify.Text(text)
        for i in range(3):
            ghostDescription += text_model.make_sentence(tries=100) + " "
        ghostCorpusFO.close()
        ghostDescription = adjective + " spirit. " + ghostDescription
        return ghostDescription

    def generateGhost(self):
        random.seed(self.seed)
        someNumber = random.randint(0, 10000)
        substance = self.getSubstance()
        kind = self.getGhostName()
        description = self.generateGhostDescription()
        self.kind = "Ghost"
        self.name = kind
        self.description = description
        self.skills = self.getSkills()

    # obelisk functions

    def generateObelisk(self):
        random.seed(self.seed)
        someNumber = random.randint(0, 10000)
        substance = self.getSubstance()
        self.kind = "Obelisk"
        self.name = "nameless obelisk"
        self.description = (
            "A " + str(someNumber) + " foot high obelisk made of " + substance + "."
        )
        self.skills = {}

    def __str__(self):
        skillsString = "\n".join(self.skills)
        return (
            "Name: "
            + str(self.name)
            + "\n \nKind: "
            + str(self.kind)
            + "\n \nDescription: "
            + str(self.description)
            + "\n \nSkills\n"
            + skillsString
        )

    # puts either an 'a' or 'an' before a word depending on if the word starts with a vowel or not and not at all if it's plural

    def addAorAn(self, word):
        if (
            word[-1] != "s"
            and word[0] == "a"
            or word[0] == "e"
            or word[0] == "i"
            or word[0] == "o"
            or word[0] == "u"
        ):
            word = "an " + word
        elif word[-1] != "s":
            word = "a " + word
        return word
