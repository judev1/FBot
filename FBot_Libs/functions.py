from datetime import datetime, timezone
from discord import Embed
import os

class fn:

    def gettoken(self, num):
        with open("./Info/Tokens.txt", "r") as file: data = file.readlines()
        return data[int(num)][:-1]

    def getinfo(self, info):
        with open("./Info/Info.txt", "r") as file: data = file.readlines()
        if info == "lastupdated": return data[0][:-1]
        elif info == "ver": return data[1][:-1]
        else: raise NameError(f"No variable called '{info}'")

    def getnotices(self):
        with open("./Info/Notices.txt", "r") as file:
            data = file.readlines()
            notices = ""
            for line in data: notices += str(line)
        return eval(notices)

    def getevents(self):
        with open("./Info/Events.txt", "r") as file:
            data = file.readlines()
            events = ""
            for line in data: events += str(line)
        return eval(events)

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

    def getcls(self, ver):
        with open(f"./Info/Change_Logs/{ver}.txt", "r") as file:
            data = file.readlines()
            cl = ""
            for line in data: cl += str(line)
        return eval(cl)

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

    def embed(self, title, *desc, url=""):
        desc = "\n".join(desc)
        return Embed(title=title, description=desc, colour=self.red, url=url)

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

class ftime:

    def __init__(self):
        self.ms, self.hs, self.ds, self.mos = self.get()

        self.start = f"{self.hs}:{self.ms}, {self.ds}/{self.mos} UTC"

    def get(self):
        time = datetime.now(tz=timezone.utc)
        m = int(time.strftime("%M"))
        h = int(time.strftime("%H"))
        d = int(time.strftime("%d"))
        mo = int(time.strftime("%m"))
        return m, h, d, mo

    def now(self):
        m, h, d, mo = self.get()
        return f"{h}:{m}, {d}-{mo} UTC"

    def uptime(self):
        ms, hs, ds, mos = self.ms, self.hs, self.ds, self.mos
        mn, hn, dn, mon = self.get()

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
