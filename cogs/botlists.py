from discord.ext import commands
import requests
import random
import os

f = "~~f~~ "

class fakeuser: id = 0
user = fakeuser()

bot_id = "711934102906994699"
bfdapi = f"https://botsfordiscord.com/api/bot/{bot_id}"
dbggapi = f"https://discord.bots.gg/api/v1/bots/{bot_id}/stats"
dblapi = f"https://discordbotlist.com/api/v1/bots/{bot_id}/stats"

class botlists(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbl = bot.dbl
        self.voteschannel = self.bot.get_channel(757722305395949572).send

    @commands.command(name="scounts")
    @commands.is_owner()
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
        headers = {"Authorization": os.getenv("BFD_TOKEN")}
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
        headers = {"Authorization": os.getenv("DBGG_TOKEN")}
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
        headers = {"Authorization": os.getenv("DBL_TOKEN")}
        res = requests.post(dblapi, data=data, headers=headers)

        if "200" in res.__str__():
            content += "\n**discordbotlist.com:** success"
            embed.description = content
        else:
            content += "\n**discordbotlist.com:** failed"
            embed.description = content
        await msg.edit(embed=embed)

    @commands.command(name="vote")
    async def _Vote(self, ctx):
        fn, db, ftime = self.bot.fn, self.bot.db, self.bot.ftime
        user = ctx.author

        embed = fn.embed(user, "FBot Vote")

        def getvalue(site):
            nextvote = db.nextvote(user.id, site)
            if nextvote:
                mins, hours = nextvote
                if not hours:
                    value = f"**{mins}m**"
                else:
                    value = f"**{hours}h** and **{mins}m**"
            else:
                value = "You can vote!"
            return value

        db.add_voter(user.id)
        embed.add_field(name="top.gg", value="[{getvalue('top')}]({fn.votetop} 'Vote here')")
        embed.add_field(name="botsfordiscord", value=f"[{getvalue('bfd')}]({fn.votebfd} 'Vote here')")
        embed.add_field(name="discordbotlist", value=f"[{getvalue('dbl')}]({fn.votedbl} 'Vote here')")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_vote(self, site, data):

        if site == "botsfordiscord.com":
            user_id = int(data["user"])
        else: user_id = int(data["id"])

        self.bot.db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"
        else: name = f"{name.mention} (*{name.name}*)"

        if site == "discordbotlist.com":
            self.bot.db.vote(user_id, "dbl")
            embed = self.bot.fn.embed(user, site, f"{name} voted")
        elif data["type"] == "test":
            embed = self.bot.fn.embed(user, site + " test", f"{name} tested out the webhook")
        elif site == "botsfordiscord.com":
            self.bot.db.vote(user_id, "bfd")
            embed = self.bot.fn.embed(user, site, f"{name} voted")
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
        else: name = f"{name.mention} (*{name.name}*)"

        self.bot.db.vote(user_id, "top")
        embed = self.bot.fn.embed(user, "top.gg", f"{name} voted")
        await self.voteschannel(embed=embed)

def setup(bot):
    bot.add_cog(botlists(bot))
