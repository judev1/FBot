from functions import predicate, fn
from discord.ext import commands
import economy as e
import requests
import random

f = "~~f~~ "

class fakeuser: id = 0
user = fakeuser()

gettoken = fn().gettoken
bot_id = "711934102906994699"
bfdapi = f"https://botsfordiscord.com/api/bot/{bot_id}"
dbggapi = f"https://discord.bots.gg/api/v1/bots/{bot_id}/stats"
dblapi = f"https://discordbotlist.com/api/v1/bots/{bot_id}/stats"

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbl = bot.dbl
        self.voteschannel = self.bot.get_channel(757722305395949572).send

    @commands.command(name="scounts")
    @commands.is_owner()
    @commands.check(predicate)
    async def _SCOUNTS(self, ctx):
        servers = len(self.bot.guilds)
        embed = self.bot.fn.embed(ctx.author, f"Server Counts `{servers}`")
        msg = await ctx.send(embed=embed)

        # top.gg
        try:
            await self.dbl.post_guild_count()
            content = "**top.gg:** success"
            embed.description = content
        except:
            content = "**tog.gg:** failed"
            embed.description = content
        await msg.edit(embed=embed)

        # botsfordiscord.com
        data = {"server_count": servers}
        headers = {"Authorization": gettoken(6)}
        res = requests.post(bfdapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**botsfordiscord.com:** success"
            embed.description = content
        else:
            content += "\n**botsfordiscord.com:** failed"
            embed.description = content
        await msg.edit(embed=embed)

        # discord.bots.gg
        data = {"guildCount": servers}
        headers = {"Authorization": gettoken(7)}
        res = requests.post(dbggapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**discord.bots.gg:** success"
            embed.description = content
        else:
            content += "\n**discord.bots.gg:** failed"
            embed.description = content
        await msg.edit(embed=embed)

        # discordbotlist.com
        data = {"guilds": servers}
        headers = {"Authorization": gettoken(8)}
        res = requests.post(dblapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**discordbotlist.com:** success"
            embed.description = content
        else:
            content += "\n**discordbotlist.com:** failed"
            embed.description = content
        await msg.edit(embed=embed)

    @commands.command(name="vote")
    @commands.check(predicate)
    async def _Vote(self, ctx):
        fn, db, ftime = self.bot.fn, self.bot.db, self.bot.ftime
        user = ctx.author
        job = db.getjob(user.id)
        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)
        salary = e.salaries[job] * jobmulti
        salary *= db.getusermulti(user.id)

        multi = 20
        if ftime.isweekend(): multi *= 2

        embed = fn.embed(user, "FBot Vote",
                         "Each site has unique voting rewards")
        def getvalue(site):
            nextvote = db.nextvote(user.id, site)
            if nextvote:
                mins, hours = nextvote
                if not hours:
                    value = f"**{mins}m**"
                else:
                    value = f"**{hours}h** and **{mins}m**"
            else:
                if site == "top":
                    value = "1x **Random FBox**"
                elif site == "bfd":
                    value = "15x **Spamables**"
                elif site == "dbl":
                    value = "10x **Spamables**"
            return value

        embed.add_field(name="top.gg", value=f"[{getvalue('top')}]({fn.votetop} 'Vote here')")
        embed.add_field(name="botsfordiscord", value=f"[{getvalue('bfd')}]({fn.votebfd} 'Vote here')")
        embed.add_field(name="discordbotlist", value=f"[{getvalue('dbl')}]({fn.votedbl} 'Vote here')")
        await ctx.send(embed=embed)

    @commands.command(name="votehs")
    @commands.check(predicate)
    async def _Votehs(self, ctx):
        await ctx.send("`fbot votehs` has moved to `fbot top votes`")

    def vote(self, user_id, site):
        self.bot.db.vote(user_id, site)
        if site == "top":
            num = random.randint(1, 100)
            if num <= 60:
                item = "cfbox"
            elif num <= 80:
                item = "ufbox"
            elif num <= 96:
                item = "rfbox"
            elif num <= 100:
                item = "lfbox"
            self.bot.db.additem(user_id, item, 1)
        elif site == "bfd":
            item = random.choice(e.spamables)
            self.bot.db.additem(user_id, item, 15)
        elif site == "dbl":
            item = random.choice(e.spamables)
            self.bot.db.additem(user_id, item, 10)
        return item

    @commands.Cog.listener()
    async def on_vote(self, site, data):

        if site == "botsfordiscord.com":
            user_id = int(data["user"])
        else: user_id = int(data["id"])

        self.bot.db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"

        if site == "discordbotlist.com":
            reward = self.vote(user_id, "dbl")
            embed = self.bot.fn.embed(user, site,
                    f"{name} voted and gained `10x {reward}`")
        elif data["type"] == "test":
            embed = self.bot.fn.embed(user, site + " test",
                    f"{name} tested out the webhook")
        elif site == "botsfordiscord.com":
            reward = self.vote(user_id, "bfd")
            embed = self.bot.fn.embed(user, site,
                    f"{name} voted and gained `15x {reward}`")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        user_id = data["user"]
        self.bot.db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"

        embed = self.bot.fn.embed(user, "top test",
                f"{name} tested out the webhook")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user_id = data["user"]
        self.bot.db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"

        reward = self.vote(user_id, "top")
        embed = self.bot.fn.embed(user, "top.gg",
                f"{name} voted and obtained `1x {reward}`")
        await self.voteschannel(embed=embed)

def setup(bot):
    bot.add_cog(economy(bot))
