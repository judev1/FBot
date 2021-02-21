from discord.ext import commands
from datetime import datetime, timezone
from discord import Embed, Client
from database import db
import commands as cm
import os

emojis = {True: "✅",
          False: "⛔"}

bot_id = 711934102906994699
db = db(verbose=False)
def cooldown(ctx):
    bot_perms = ctx.channel.permissions_for(ctx.guild.get_member(bot_id))

    valid = []
    perms = {}
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

    usercooldown = db.Get_Cooldown(ctx.author.id)
    if usercooldown > 0:
        raise commands.CommandOnCooldown(commands.BucketType.user,
                                         usercooldown)
    return True

class fn:

    def gettoken(self, num):
        if num == 1:
            print(f"""
################################################
# /!\ YOU ARE RUNNING ON FBOT'S MAIN TOKEN /!\ #
################################################
# /!\ YOU ARE RUNNING ON FBOT'S MAIN TOKEN /!\ #
################################################
# /!\ YOU ARE RUNNING ON FBOT'S MAIN TOKEN /!\ #
################################################\n\n""")
        with open("./Info/Tokens.txt", "r") as file: data = file.readlines()
        return data[int(num)][:-1]

    def getinfo(self, info):
        with open("./Info/Info.txt", "r") as file: data = file.readlines()
        if info == "lastupdated": return data[0][:-1]
        elif info == "ver": return data[1][:-1]
        else: raise NameError(f"No variable called '{info}'")

    def getcogs(self):
        cogs = []
        for cog in os.listdir("FBot_Cogs"):
            if os.path.isfile(os.path.join("FBot_Cogs", cog)):
                cogs.append(cog)
        return cogs

    def getvers(self):
        vers = []
        for ver in os.listdir("Info/Change_Logs"):
            if os.path.isfile(os.path.join("Info/Change_Logs", ver)):
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
    
    red = 0xF42F42
    
    top = "https://top.gg/bot/711934102906994699"
    dbl = "https://discordbotlist.com/bots/fbot"
    votetop = "https://top.gg/bot/711934102906994699/vote"
    votedbl = "https://discordbotlist.com/bots/fbot/upvote"

    site = "https://fbot.breadhub.uk"
    server = "https://fbot.breadhub.uk/server"
    invite = "https://fbot.breadhub.uk/invite"
    github = "https://github.com/judev1/FBot"
    fbot = "https://cdn.discordapp.com/icons/717735765936701450/b2649caffd40fae44442bec642b69efd.webp?size=1024"

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
        if fn().gettoken(5) == auth:
            data = await request.json()
            self.bot.dispatch("vote", data)
            return web.Response(status=200)
        return web.Response(status=401)

class ftime:

    def __init__(self):
        time = datetime.now(tz=timezone.utc)
        self.ms, self.hs, self.ds, self.mos = [int(i) for i in time.strftime("%M %H %d %m").split()]

        self.start = self.now()

    def now(self):
        time = datetime.now(tz=timezone.utc)
        return time.strftime("%H:%M, %d/%m/%y UTC")

    def isweekend(self):
        return datetime.now().strftime("%a") in ["Sat", "Sun"]

    def uptime(self):
        time = datetime.now(tz=timezone.utc)
        ms, hs, ds, mos = self.ms, self.hs, self.ds, self.mos
        mn, hn, dn, mon = [int(i) for i in time.strftime("%M %H %d %m").split()]

        if mos > mon:
            mo = 60 - mos + mon
        else: mo = mon - mos
        
        if ds > dn:
            if mos == 2:
                d = 28 - ds
            elif mos in [4, 6, 9, 10]:
                d = 30 - ds
            else:
                d = 31 - ds
            d += dn
            m -= 1
        else: d = dn - ds

        if hs > hn:
            h = 24 - hs + hn
            d -= 1
        else: h = hn - hs

        if ms > mn:
            m = 60 - ms + mn
            h -= 1
        else: m = mn - ms

        dp, hp, mp = "s", "s", "s"
        if d in [0, 1]: dp = ""
        if h in [0, 1]: hp = ""
        if m in [0, 1]: mp = ""
        
        if d > 0:
            uptime = f"{d} day{dp}, {h} hour{hp}"
        elif h > 0:
            uptime = f"{h} hour{hp}, {m} minute{mp}"
        else: uptime = f"{m} minute{mp}"

        return uptime
