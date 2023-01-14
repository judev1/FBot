from random import choice
import json

with open("data/replacements.json", "r", encoding="utf-8") as file:
    maps = json.load(file)

class PirateInsults:
    def __repr__(self):
        pirate = maps['pirate']
        return f"{choice(pirate['adjectives'])} {choice(pirate['insults'])}"
pirate_insult = PirateInsults

def sanitise_text(text):
    text = text.replace('“', '"')
    text = text.replace("’", "'")
    return text

def capitalise(text):
    return text[0].upper() + text[1:]

def replace_words(text, words):
    for old, new in words:
        new_text = list()
        for word in text.split(" "):
            if old == word:
                new_text.append(new)
            elif old.capitalize() == word:
                new_text.append(new[0].upper() + new[1:])
            elif old.upper() == word:
                new_text.append(new.upper())
            else:
                new_text.append(word)
        text = " ".join(new_text)
    return text

def replace_starts(text, words):
    for old, new in words:
        new_text = list()
        for word in text.split(" "):
            if not old:
                new_text.append(new + word)
            elif word.startswith(old):
                new_text.append(new + word[len(old):])
            elif word.startswith(old.capitalize()):
                new_text.append(new[0].upper() + new[1:] + word[len(old):])
            elif word.startswith(old.upper()):
                new_text.append(new.upper() + word[len(old):])
            else:
                new_text.append(word)
        text = " ".join(new_text)
    return text

def replace_ends(text, words):
    for old, new in words:
        new_text = list()
        for word in text.split(" "):
            if not old:
                new_text.append(word + new)
            elif word.endswith(old):
                new_text.append(word[:-len(old)] + new)
            elif word.endswith(old.capitalize()):
                new_text.append(word[:-len(old)] + new[0].upper() + new[1:])
            elif word.endswith(old.upper()):
                new_text.append(word[:-len(old)] + new.upper())
            else:
                new_text.append(word)
        text = " ".join(new_text)
    return text

def replace_chars(text, letters):
    for old, new in letters:
        if old in text:
            text = text.replace(old, new)
        elif old.capitalize() in text:
            text = text.replace(old.capitalize(), new[0].upper() + new[1:])
        elif old.upper() in text:
            text = text.replace(old.upper(), new.upper())
    return text

def uwu(text):
    settings = maps["uwu"]
    text = replace_chars(text, settings["chars"])
    return text + choice(settings["tails"])

def pirate(text):
    settings = maps["pirate"]
    insults = map(lambda x: (x, pirate_insult), maps["insults"])
    text = replace_words(text, settings["words"])
    text = replace_words(text, insults)
    text = replace_starts(text, settings["starts"])
    text = replace_ends(text, settings["ends"])
    text = replace_chars(text, settings["chars"])
    return text + choice(settings["tails"])

def biblical(text):
    settings = maps["biblical"]
    text = replace_words(text, settings["words"])
    text = replace_ends(text, settings["ends"])
    text = replace_chars(text, settings["chars"])
    return text

def roadman(text):
    settings = maps["roadman"]
    text = replace_words(text, settings["words"])
    text = replace_starts(text, settings["starts"])
    text = replace_chars(text, settings["chars"])
    text = choice(settings["heads"]) + text
    return text + choice(settings["tails"])

def australian(text):
    settings = maps["australian"]
    text = "G'day " + text
    print(text)
    text = text[::-1]
    for old, new in settings["chars"]:
        text = text.replace(old, new)
    return text

def german(text):
    # might be funny to check for nouns with adjectives in front of them and make them a
    # single word
    settings = maps["german"]
    text = replace_words(text, settings["words"])
    text = replace_starts(text, settings["starts"])
    text = replace_ends(text, settings["ends"])
    text = replace_chars(text, settings["chars"])
    return text

def italian(text):
    settings = maps["italian"]
    text = replace_ends(text, settings["ends"])
    return f"*{text}*"

def safe(text):
    settings = maps["safe"]
    text = replace_words(text, settings["words"])
    return text

def fuck(text):
    new_text = []
    for word in text.split():
        if choice([0, 0, 1]):
            word = "fucking " + word
        new_text.append(word)
    return " ".join(new_text)

def triggered(text):
    return f"**{text.upper()}**"

def ironic(text):
    new_text = ""
    for char in text:
        new_text += choice([char.lower(), char.upper()])
    return new_text

def patronise(text):
    return " ".join(text)

def confused(text):
    settings = maps["confused"]
    text = replace_words(text, settings["words"])
    text = replace_ends(text, settings["ends"])
    return text + choice(settings["tails"])

def safe(text):
    settings = maps["safe"]
    text = replace_words(text, settings["words"])
    return text