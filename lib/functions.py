import json
import os

import lib.database as db
from lib.votinghandler import VotingHandler
from lib.ftime import ftime

emojis = {True: "✅", False: "⛔"}

def formatperm(perm):
    text = list()
    perm = perm.lower()
    for word in perm.split("_"):
        if word.startswith("("):
             text.append(word[0:2].upper() + word[2:])
        else:
            text.append(word[0].upper() + word[1:])
    return " ".join(text)

def getprefix(bot, message):
    if not bot.ready():
        return "fbot"
    prefix = "fbot"
    if str(message.channel.type) != "private":
        prefix = db.getprefix(message.guild.id)
    if prefix == "fbot":
        content = message.content
        if content[:5].lower() == "fbot ": prefix = content[:5]
        elif content[:6].lower() == "f bot ": prefix = content[:6]
        elif content[:23].lower() == "<@!711934102906994699> ":
            prefix = content[:6]
    if not message.author.bot:
        db.register(message.author.id)
    return prefix

def getcommand(bot, message, ignore_dev=False, commands=list(), cogs=list()):

    def in_commands(command):
        if command.name in commands:
            return True
        for alias in command.aliases:
            if alias in commands:
                return True
        return False

    prefix = getprefix(bot, message)
    without_prefix = message.content[len(prefix):]

    for command in bot.commands:
        if cogs and in_commands(command):
            continue
        elif commands and command.cog.qualified_name in cogs:
            continue
        elif ignore_dev and command.cog.qualified_name == "dev":
            continue
        if without_prefix.startswith(command.name):
            return command
        for alias in command.aliases:
            if without_prefix.startswith(alias):
                return command

def getcogs():
    cogs = list()
    for cog in os.listdir("cogs"):
        if os.path.isfile(os.path.join("cogs", cog)):
            cogs.append(cog)
    return cogs

def formatname(name):
    if not name:
        name = "Deleted User"
    else:
        name = name.name.replace("*", "")
        name = name.replace("`", "")
        name = name.replace("_", "")
        name = name.replace("||", "")
    return name

class Classify:

    def __init__(self, dictionary: dict):
        for name in dictionary:
            value = dictionary[name]
            if type(value) is dict:
                value = Classify(value)
            self[name] = value

    def __repr__(self):
        return str(self.__dict__)

    def __iter__(self):
        for item in self.__dict__:
            yield item

    def __getitem__(self, item):
        if item in self.__dict__:
            return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

class ShellObject: id = -1
user = guild = ShellObject()

with open("data/data.json", "r") as file:
    data = Classify(json.load(file))
    links = data.links

for colour in data.colours:
    data.colours[colour] = int(data.colours[colour], 16)

with open("./data/colours.json", "r") as file:
    colours = json.load(file)
with open("./data/customcolours.json", "r") as file:
    custom_colours = json.load(file)

for colour in custom_colours:
    colours[colour] = custom_colours[colour]

colour_names = list(colours)
hex_values = list(colours.values())
colour_values = dict()
for colour, value in zip(colour_names, hex_values):
    colour_values[value] = colour