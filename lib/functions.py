from discord.ext import commands
from discord import Embed
import commands as cm
from cache import *
import os

emojis = {True: "✅",
          False: "⛔"}

def predicate(ctx):
    if str(ctx.channel.type) != "private":
        bot_perms = ctx.channel.permissions_for(ctx.guild.get_member(bot_id))

        valid, perms = [], {}
        for perm in cm.perms[ctx.command.name]:
            if not perm.startswith("("):
                bot_perm = getattr(bot_perms, perm)
            else: bot_perm = True
            valid.append(bot_perm)
            perms[perm] = bot_perm

        if not all(valid):
            page = "**Missing permissions to run this command**\n\n"
            for perm in perms:
                if perm.startswith("("):
                    perms[perm] = getattr(bot_perms, perm[1:-1])
                page += f"{emojis[perms[perm]]} ~ {perm.upper()}\n"
            raise commands.CheckFailure(message=page)
    else:
        if cm.commands[ctx.command.name][5] == "*Yes*":
            raise commands.NoPrivateMessage()

    cooldown = cache["Cooldowns"].cooldown(ctx)
    if cooldown:
        raise commands.CommandOnCooldown(commands.BucketType.user, cooldown)
    return True

class fn:

    def setbot(self, bot):
        self.bot = bot

        global cache, bot_id
        bot_id = bot.user.id
        bot.cache = dict()
        cache = bot.cache

        bot.cache["Cooldowns"] = Cooldowns()
        bot.cache["Names"] = Names()
        bot.cache["RateLimits"] = RateLimits()

    def getinfo(self, info):
        with open("./data/Info.txt", "r") as file: data = file.readlines()
        if info == "lastupdated": return data[0][:-1]
        elif info == "ver": return data[1][:-1]
        else: raise NameError(f"No variable called '{info}'")

    def getcogs(self):
        cogs = []
        for cog in os.listdir("cogs"):
            if os.path.isfile(os.path.join("cogs", cog)):
                cogs.append(cog)
        return cogs

    def getvers(self):
        vers = []
        for ver in os.listdir("data/Change_Logs"):
            if os.path.isfile(os.path.join("data/Change_Logs", ver)):
                vers.append(ver[:-4])
        return sorted(vers, reverse=True)

    def getprefix(self, bot, message):
        prefix = "fbot"
        if str(message.channel.type) != "private":
            prefix = bot.db.Get_Prefix(message.guild.id)
        if prefix == "fbot":
            content = message.content
            if content[:5].lower() == "fbot ": prefix = content[:5]
            elif content[:6].lower() == "f bot ": prefix = content[:6]
            elif content[:23].lower() == "<@!711934102906994699> ":
                prefix = content[:6]
        if not message.author.bot:
            bot.db.register(message.author.id)
        if bot.db.isBanned(message.author.id):
            return False
        return prefix

    def checkchars(self, prefix):
        bannedchars = list("{}()[]\"'`")
        for char in prefix:
            for bannedchar in bannedchars:
                if bannedchar == char: return char
            return None

    def embed(self, user, title, *desc, url=""):
        colour = self.bot.db.getcolour(user.id)
        desc = "\n".join(desc)
        return Embed(title=title, description=desc, colour=colour, url=url)

    def errorembed(self, error, info):
        return Embed(title=f"**Error:** `{error}`",
               description=f"```{info}```", colour=self.red)

    def formatname(name):
    if not name:
        name = "Deleted User"
        else:
            name = name.name.replace("*", "")
            name = name.replace("`", "")
            name = name.replace("_", "")
            name = name.replace("||", "")
        return name

    red = 0xF42F42

    top = "https://top.gg/bot/711934102906994699"
    dbl = "https://discordbotlist.com/bots/fbot"
    bfd = "https://botsfordiscord.com/bot/711934102906994699"
    dbgg = "https://discord.bots.gg/bots/711934102906994699"

    votetop = "https://top.gg/bot/711934102906994699/vote"
    votedbl = "https://discordbotlist.com/bots/fbot/upvote"
    votebfd = "https://botsfordiscord.com/bot/711934102906994699/vote"

    site = "https://fbot.breadhub.uk"
    server = "https://fbot.breadhub.uk/server"
    invite = "https://fbot.breadhub.uk/invite"
    github = "https://github.com/judev1/FBot"
    banner = "https://fbot.breadhub.uk/banner"

from discord import Client
from aiohttp import web
import asyncio

class voting_handler:

    def __init__(self, bot: Client):

        async def start():
            app = web.Application(loop=self.bot.loop)
            app.router.add_post("/vote", self.on_post_request)

            runner = web.AppRunner(app)
            await runner.setup()

            server = web.TCPSite(runner, '0.0.0.0', 2296)
            await server.start()

        self.bot = bot

        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())

    async def on_post_request(self, request):
        auth = request.headers.get("Authorization")
        if "dbl_" + os.getenv("DBL_TOKEN") == auth:
            site = "discordbotlist.com"
        elif "bfd_" + os.getenv("BFD_TOKEN") == auth:
            site = "botsfordiscord.com"
        else:
            return web.Response(status=401)

        data = await request.json()
        self.bot.dispatch("vote", site, data)
        return web.Response(status=200)

from datetime import datetime, timezone

class ftime:

    def __init__(self):
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