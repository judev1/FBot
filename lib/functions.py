import json
import os

from lib.votinghandler import VotingHandler
from lib.ftime import ftime

emojis = {True: "✅", False: "⛔"}

def formatperm(perm):
    text = []
    perm = perm.lower()
    for word in perm.split("_"):
        if word.startswith("("):
             text.append(word[0:2].upper() + word[2:])
        else:
            text.append(word[0].upper() + word[1:])
    return " ".join(text)

async def getprefix(bot, message):
    if not bot.ready():
        return "fbot"
    prefix = "fbot"
    if str(message.channel.type) != "private":
        prefix = await bot.db.getprefix(message.guild.id)
    if prefix == "fbot":
        content = message.content
        if content[:5].lower() == "fbot ": prefix = content[:5]
        elif content[:6].lower() == "f bot ": prefix = content[:6]
        elif content[:23].lower() == "<@!711934102906994699> ":
            prefix = content[:6]
    if not message.author.bot:
        await bot.db.register(message.author.id)
    return prefix

def getcogs():
    cogs = []
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
    colours = data.colours
    links = data.links

for colour in colours:
    colours[colour] = int(colours[colour], 16)