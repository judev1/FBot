from functions import cooldown, fn
from discord.ext import commands
import economy as e
import requests
import discord
import dbl

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
    @commands.check(cooldown)
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
                         "If you vote you'll earn your salary without tax",
                         f"So {fn.fnum(salary)} if I'm not mistaken",
                         f"AND multiplier worth **{multi} messages**!\n",

                         f"[top.gg vote]({fn.votetop})",
                         f"[botsfordiscord.com]({fn.votebfd})",
                         f"[discordbotlist.com]({fn.votedbl}) (No rewards)")
        await ctx.send(embed=embed)

    def vote_rewards(self, user_id, count):
        for i in range(count):
            db = self.bot.db
            
            job = db.getjob(user_id)
            if job == "Unemployed": jobmulti = 1.0
            else: jobmulti = db.getjobmulti(user_id)
            salary = e.salaries[job] * jobmulti
            salary = round(salary * db.getusermulti(user_id))
            db.updatebal(user_id, salary)

            bonus = 1
            if self.bot.ftime.isweekend(): bonus = 2
            db.increasemultiplier(user_id, 0, 20 * bonus)
        return salary * count

    @commands.Cog.listener()
    async def on_vote(self, site, data):

        if site == "botsfordiscord.com":
            user_id = int(data["user"])
        else: user_id = int(data["id"])

        self.bot.db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"

        if site == "discordbotlist.com":
            self.bot.db.vote(user_id, "dbl")
            embed = self.bot.fn.embed(user, "discordbotlist.com",
                    f"{name} voted for FBot!")
        elif data["type"] == "test":
            embed = self.bot.fn.embed(user, site + " test",
                    f"{name} tested out the webhook")
        elif site == "botsfordiscord.com":
            self.bot.db.vote(user_id, "bfd")
            salary = self.vote_rewards(user_id, 1)
            embed = self.bot.fn.embed(user, site,
                    f"{name} voted and gained {self.bot.fn.fnum(salary)}")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        user_id = data["user"]
        self.bot.db.register(user_id)
        #try: name = await self.bot.fetch_user(user_id).name
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"
            
        embed = self.bot.fn.embed(user, "top test",
                f"{name} tested out the webhook")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user_id = data["user"]
        self.bot.db.vote(user_id, "top")
        self.bot.db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"

        salary = self.vote_rewards(user_id, 1)
        embed = self.bot.fn.embed(user, "top.gg",
                f"{name} voted and gained {self.bot.fn.fnum(salary)}")
        await self.voteschannel(embed=embed)

    @commands.command(name="votehs")
    @commands.check(cooldown)
    async def _Votehs(self, ctx):
        
        message = []
        async with ctx.channel.typing():
            c = self.bot.db.conn.cursor()
            c.execute(f"SELECT user_id, topvotes FROM votes ORDER BY "
                      "topvotes DESC LIMIT 5")
            for rank, row in enumerate(c):
                user_id, votes = row
                name = await self.bot.fetch_user(user_id)
                if not name: name = "User"
                message.append(f"{rank+1}. **{name}** with **{votes} votes**")
        embed = self.bot.fn.embed(user, "Top votes this month", *message)
        await ctx.send(embed=embed)

    @commands.command(name="monthly")
    @commands.is_owner()
    async def monthly_winners(self, ctx):
        
        message = []
        async with ctx.channel.typing():
            c = self.bot.db.conn.cursor()
            c.execute(f"SELECT user_id, topvotes FROM votes ORDER BY "
                      "topvotes DESC LIMIT 3")
            for rank, row in enumerate(c):
                user_id, votes = row
                name = await self.bot.fetch_user(user_id)
                if not name: name = "User"
                if rank == 0:
                    salary = self.vote_rewards(user_id, 5)
                elif rank == 1:
                    salary = self.vote_rewards(user_id, 4)
                elif rank == 2:
                    salary = self.vote_rewards(user_id, 3)
                message.append(f"{rank+1}. **{name}** with **{votes} votes**" +
                               f" earned {self.bot.fn.fnum(salary)}\n")
        c.execute(f"UPDATE votes SET topvotes=0, dblvotes=0, bfdvotes=0")
        embed = self.bot.fn.embed(user, "FBot Monthly rewards", *message)
        await ctx.send(embed=embed)
        
    
def setup(bot):
    bot.add_cog(economy(bot))
