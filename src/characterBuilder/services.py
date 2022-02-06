from random import choice, choices, randint

import markovify


class BaseCharacterGeneration:
    kind = "unknown"
    selection_weight = 2
    name_list = "word_list.txt"
    description_corpus = "word_list.txt"
    skills_count = 4
    markovify_newline = False
    description_sentences = (
        ("_short", (140,)),
    )
    color_list = "word_lists/colors.txt"
    adjective_list = "word_lists/adjectives.txt"
    substance_list = "word_lists/substances.txt"
    description_default = "It is very mysterious. "

    def _text_model(self, *, word_list=None, newline=False):
        with open(word_list) as f:
            text = f.read()
        if newline:
            base = markovify.NewlineText(text)
        else:
            base = markovify.Text(text)
        return base.compile()

    def _choose_from_file(self, name_list, *, exclude=None):
        if exclude is None:
            exclude = []
        with open(name_list) as f:
            choices = f.readlines()
        while (chosen := choice(choices).strip(" \n")) in exclude:
            pass
        return chosen

    def name(self):
        return self._choose_from_file(self.name_list)

    def _description(self, *, name=None):
        text_model = self._text_model(
            word_list=self.description_corpus,
            newline=self.markovify_newline,
        )
        description = ""
        for length_mod, args in self.description_sentences:
            method = getattr(text_model, f"make{length_mod}_sentence")
            try:
                description += method(*args, tries=100) + " "
            except TypeError:
                description += self.description_default
                break
        return description

    def description(self, *, name=None):
        return self._description()

    def skills(self):
        skills = {}
        for _ in range(self.skills_count):
            skill = self._choose_from_file("word_lists/skills.txt")
            skills[skill] = randint(-10, 18)
        return skills

    def add_a_or_an(self, word):
        if word[-1] != "s":
            if word[0] in "aeiou":
                return f"an {word}"
            else:
                return f"a {word}"
        return word

    def adjective(self, *, exclude=None):
        return self._choose_from_file(self.adjective_list, exclude=exclude)

    def substance(self, *, exclude=None):
        return self._choose_from_file(self.substance_list, exclude=exclude)

    def color(self, *, exclude=None):
        return self._choose_from_file(self.color_list, exclude=exclude)


class GhostCharacterGeneration(BaseCharacterGeneration):
    kind = "Ghost"
    name_list = "word_lists/ghostType.txt"
    description_corpus = "word_lists/ghost_corpus.txt"
    description_sentences = (("", ()), ("", ()), ("", ()),)

    def description(self, *, name=None):
        return f"{self.add_a_or_an(self.adjective())} spirit. {self._description()}"


class RobotCharacterGeneration(BaseCharacterGeneration):
    kind = "Robot"
    name_list = "word_lists/robotName.txt"
    description_corpus = "word_lists/robot_corpus.txt"
    description_sentences = (("", ()), ("", ()), ("", ()), ("", ()),)

    def name(self):
        return f"{super().name()}-{randint(100,1000)}"

    def description(self, *, name=None):
        return f"A hard working robot. {self._description()}"


class BirdCharacterGeneration(BaseCharacterGeneration):
    kind = "Bird"
    name_list = "word_lists/birdName.txt"
    description_corpus = "word_lists/bird_corpus.txt"
    description_sentences = (("", ()), ("", ()), ("", ()),)
    markovify_newline = True

    def description(self, *, name=None):
        enemy = self._choose_from_file("word_lists/firstnames.txt")
        _type = self._choose_from_file("word_lists/animals.txt")
        return (
            f"{self._description()} {name} the bird has been hunted through life "
            f"by its enemy, {enemy}, {self.add_a_or_an(self.adjective())} "
            f"{_type}."
        )


class AnimalCharacterGeneration(BaseCharacterGeneration):
    kind = "Animal"
    name_list = "word_lists/firstnames.txt"
    description_corpus = "word_lists/animal_corpus.txt"
    description_sentences = (("_short", (140,)), ("", ()), ("", ()),)
    description_default = "It hunts daily for food. "

    def description(self, *, name=None):
        _type = (
            f"{self.add_a_or_an(self.adjective())} "
            f"{self._choose_from_file('word_lists/animals.txt')}"
        )
        return f"{_type.capitalize()} {self._description()}"


class HumanCharacterGeneration(BaseCharacterGeneration):
    kind = "Human"
    selection_weight = 4

    def name(self):
        return (
            f"{self._choose_from_file('word_lists/firstnames.txt')} " +
            self._choose_from_file("word_lists/lastnameBeginnings.txt") +
            self._choose_from_file("word_lists/lastnameEndings.txt")
        )

    def description(self, *, name=None):
        adjectives = []
        adjectives.append(self.adjective(exclude=adjectives))
        adjectives.append(self.adjective(exclude=adjectives))
        return (
            "A bipedal mammal with smooth skin and " +
            self._choose_from_file("word_lists/hair.txt") +
            f" hair on its head. It is wearing {self.add_a_or_an(self.color())} "
            f"{self._choose_from_file('word_lists/clothes.txt')}. "
            f"{name} worked as " +
            self.add_a_or_an(self._choose_from_file("word_lists/careers.txt")) +
            f" before embarking on their {adjectives[0]} quest to find the "
            f"legendary {self.substance()} obelisk. They are followed by their "
            f"faithful compainion {self._choose_from_file('word_lists/firstnames.txt')}"
            f" the {adjectives[1]} "
            f"{self._choose_from_file('word_lists/animals.txt')}. "
        )


# INANIMATE!

class InanimateCharacterGeneration(BaseCharacterGeneration):
    skills_count = 0
    selection_weight = 1


class ObeliskCharacterGeneration(InanimateCharacterGeneration):
    """The simplest character kind"""
    kind = "Obelisk"

    def name(self):
        return "Nameless obelisk"

    def description(self, *, name=None):
        return f"A {randint(0, 10000)} foot high obelist made of {self.substance()}."


class FungusCharacterGeneration(InanimateCharacterGeneration):
    kind = "Fungus"
    name_list = "word_lists/fungiName.txt"

    def description(self, *, name=None):
        _type = self._choose_from_file("word_lists/fungiType.txt")
        return f"A colony of {self.adjective()}, {self.color()} {_type}."

class VegetableCharacterGeneration(InanimateCharacterGeneration):
    kind = "Vegetable"
    description_corpus = "word_lists/veggie_corpus.txt"
    description_sentences = (("", ()), ("", ()),)
    markovify_newline = True

    def name(self):
        return "nameless vegetable"

    def description(self, *, name=None):
        _bin = choice(["pumpkin", "vegetable"])
        _type = self._choose_from_file(f"word_lists/{_bin}s.txt")
        return f"{self.add_a_or_an(self.color())} {_type}. {self._description()}"


class CharacterGeneratorService:
    generation_classes = (
        HumanCharacterGeneration,
        FungusCharacterGeneration,
        VegetableCharacterGeneration,
        AnimalCharacterGeneration,
        BirdCharacterGeneration,
        ObeliskCharacterGeneration,
        GhostCharacterGeneration,
        RobotCharacterGeneration,
    )

    def generate(self, *, generation_class=None):
        if generation_class is None:
            generation_class = choices(
                self.generation_classes,
                weights=(c.selection_weight for c in self.generation_classes)
            )[0]
        generator = generation_class()
        name = generator.name()
        return {
            "name": name,
            "kind": generation_class.kind,
            "description": generator.description(name=name),
            "skills": generator.skills(),
        }

