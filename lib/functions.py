red = 0xF42F42

top = "https://top.gg/bot/711934102906994699"
dbl = "https://discordbotlist.com/bots/fbot"

bfd = "https://discords.com/bots/bot/711934102906994699"
dbgg = "https://discord.bots.gg/bots/711934102906994699"

ligg = "https://listcord.gg/bot/711934102906994699"
dbeu = "https://discord-botlist.eu/bots/711934102906994699"

blsp = "https://botlist.space/bot/711934102906994699"
blme = "https://botlist.me/bots/711934102906994699"

yabl = "https://yabl.xyz/bot/711934102906994699"
bdcl = "https://bots.discordlabs.org/bot/711934102906994699"

votetop = "https://top.gg/bot/711934102906994699/vote"
votedbl = "https://discordbotlist.com/bots/fbot/upvote"
votebfd = "https://discords.com/bots/bot/711934102906994699/vote"

voteligg = "https://listcord.gg/bot/711934102906994699"
votedbeu = "https://discord-botlist.eu/bots/711934102906994699/vote"
voteblsp = "https://discordlist.space/bot/711934102906994699/upvote"
voteblme = "https://botlist.me/bots/711934102906994699/vote"

site = "https://fbot.breadhub.uk"
server = "https://fbot.breadhub.uk/server"
invite = "https://fbot.breadhub.uk/invite"
github = "https://github.com/judev1/FBot"
patreon = "https://www.patreon.com/fbotbot"

import lib.database as db
import os

def formatperm(perm):
    text = []
    perm = perm.lower()
    for word in perm.split("_"):
        if word.startswith("("):
             text.append(word[0:2].upper() + word[2:])
        else:
            text.append(word[0].upper() + word[1:])
    return " ".join(text)

def getprefix(bot, message):
    if not bot.ready:
        return "f" * 4097
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

def getcogs():
    cogs = []
    for cog in os.listdir("cogs"):
        if os.path.isfile(os.path.join("cogs", cog)):
            cogs.append(cog)
    return cogs

from discord import Client
from aiohttp import web
import asyncio
import logging

logging.getLogger("aiohttp.server").setLevel(logging.CRITICAL)

class VotingHandler:

    def __init__(self, bot: Client):

        async def start():
            app = web.Application(loop=self.bot.loop)
            app.router.add_post("/vote", self.on_post_request)

            runner = web.AppRunner(app)
            await runner.setup()

            server = web.TCPSite(runner, "0.0.0.0", 2296)
            await server.start()

        self.bot = bot

        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())

    async def on_post_request(self, request):
        auth = request.headers.get("Authorization")
        if "dbl_" + os.getenv("WEBHOOK_AUTH") == auth:
            site = "discordbotlist.com"
        elif "bfd_" + os.getenv("WEBHOOK_AUTH") == auth:
            site = "botsfordiscord.com"
        else:
            return web.Response(status=401)

        data = await request.json()
        self.bot.dispatch("vote", site, data)
        return web.Response(status=200)

from datetime import datetime, timezone

class ftime:

    def __init__(self):
        self.set()

    def set(self):

        time = datetime.now(tz=timezone.utc)
        self.min_start, self.hour_start, self.day_start, self.month_start = [int(i) for i in time.strftime("%M %H %d %m").split()]
        self.start = self.now()

    def now(self):
        time = datetime.now(tz=timezone.utc)
        return time.strftime("%H:%M, %d/%m/%y UTC")

    def isweekend(self):
        return datetime.now().strftime("%a") in ["Sat", "Sun"]

    def uptime(self):
        time = datetime.now(tz=timezone.utc)
        min_start, hour_start, day_start, month_start = self.min_start, self.hour_start, self.day_start, self.month_start
        min_now, hour_now, day_now, month_now = [int(i) for i in time.strftime("%M %H %d %m").split()]

        if month_start > month_now:
            months = 60 - month_start + month_now
        else: months = month_now - month_start

        if day_start > day_now:
            if month_start == 2:
                days = 28 - day_start
            elif month_start in [4, 6, 9, 10]:
                days = 30 - day_start
            else:
                days = 31 - day_start
            days += day_now
            months -= 1
        else: days = day_now - day_start

        if hour_start > hour_now:
            hours = 24 - hour_start + hour_now
            days -= 1
        else: hours = hour_now - hour_start

        if min_start > min_now:
            mins = 60 - min_start + min_now
            hours -= 1
        else: mins = min_now - min_start

        days_plural, hours_plural, mins_plural = "s", "s", "s"
        if days == 1: days_plural = ""
        if hours == 1: hours_plural = ""
        if mins == 1: mins_plural = ""

        if days > 0:
            uptime = f"{days} day{days_plural}, {hours} hour{hours_plural}"
        elif hours > 0:
            uptime = f"{hours} hour{hours_plural}, {mins} minute{mins_plural}"
        else: uptime = f"{mins} minute{mins_plural}"

        return uptime