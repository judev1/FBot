from discord.ext import commands
import lib.functions as fn
import lib.database as db
import aiohttp

class fakeuser: id = 0
user = fakeuser()

bot_id = "711934102906994699"
bfdapi = f"https://discords.com/bots/api/bot/{bot_id}"
dbggapi = f"https://discord.bots.gg/api/v1/bots/{bot_id}/stats"
dblapi = f"https://discordbotlist.com/api/v1/bots/{bot_id}/stats"

class Botlists(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.dbl = bot.dbl

    @commands.Cog.listener()
    async def on_bot_ready(self):
        voteschannel = self.bot.settings.channels.votes
        self.voteschannel = self.bot.get_channel(voteschannel)

    @commands.command()
    async def scounts(self, ctx):
        tokens = self.bot.settings.tokens
        servers = len(self.bot.guilds)
        embed = self.bot.embed(ctx.author, f"Server Counts `{servers}`")
        msg = await ctx.send(embed=embed)
        session = aiohttp.ClientSession()

        # top.gg
        try:
            await self.dbl.post_guild_count()
            content = "**top.gg:** success"
        except:
            content = "**tog.gg:** failed"
        embed.description = content
        await msg.edit(embed=embed)

        # discords.com/bots
        data = {"server_count": servers}
        headers = {"Authorization": tokens.bfd}
        async with session.post(bfdapi, data=data, headers=headers) as res:
            content += "\n**discords.com/bots:** " + ("success" if res.status == 200 else "failed")
            embed.description = content
        await msg.edit(embed=embed)

        # discord.bots.gg
        data = {"guildCount": servers}
        headers = {"Authorization": tokens.dbgg}
        async with session.post(dbggapi, data=data, headers=headers) as res:
            content += "\n**discord.bots.gg:** " + ("success" if res.status == 200 else "failed")
            embed.description = content
        await msg.edit(embed=embed)

        # discordbotlist.com
        data = {"guilds": servers}
        headers = {"Authorization": tokens.dbl}
        async with session.post(dblapi, data=data, headers=headers):
            content += "\n**discordbotlist.com:** " + ("success" if res.status == 200 else "failed")
            embed.description = content
        await msg.edit(embed=embed)

        await session.close()

    @commands.command()
    async def vote(self, ctx):
        user = ctx.author
        embed = self.bot.embed(user, "FBot Vote")

        def get_value(site):
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

        db.addvoter(user.id)
        embed.add_field(name=":mailbox_with_mail:  **__SAVED__**", inline=False, value="Your votes appear in your profile and on leaderboards")
        embed.add_field(name="top.gg", value=f"[{get_value('top')}]({fn.votetop} 'Vote here')")
        embed.add_field(name="discords.com/bots", value=f"[{get_value('bfd')}]({fn.votebfd} 'Vote here')")
        embed.add_field(name="discordbotlist", value=f"[{get_value('dbl')}]({fn.votedbl} 'Vote here')")

        embed.add_field(name=":mailbox_closed: **__NOT SAVED__**", inline=False, value="Your votes do not appear in your profile or on leaderboards")
        embed.add_field(name="listcord.gg", value=f"[Vote here]({fn.voteligg} 'Please sign in first then and vote on this page')")
        embed.add_field(name="discord-botlist.eu", value=f"[Vote here]({fn.votedbeu} 'Vote here')")
        embed.add_field(name="botlist.space", value=f"[Vote here]({fn.voteblsp} 'Vote here')")
        embed.add_field(name="botlist.me", value=f"[Vote here]({fn.voteblme} 'Vote here')")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_vote(self, site, data):

        if site == "discords.com":
            user_id = int(data["user"])
        elif site == "discordbotlist.com":
            user_id = int(data["id"])
        else:
            embed = self.bot.embed(user, site, "Someone used a webhook")
            await self.voteschannel.send(embed=embed)
            return

        db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = f"<@{user_id}> [unknown]"
        else: name = f"{name.mention} (*{name.name}*)"

        if site == "discords.com":
            if data["type"] == "vote":
                db.vote(user_id, "bfd")
                embed = self.bot.embed(user, site, f"{name} voted")
            elif data["type"] == "test":
                embed = self.bot.embed(user, site + " test", f"{name} tested out the webhook")
        elif site == "discordbotlist.com":
            db.vote(user_id, "dbl")
            embed = self.bot.embed(user, site, f"{name} voted")
        await self.voteschannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        user_id = data["user"]
        db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"

        embed = self.bot.embed(user, "top test",
                f"{name} tested out the webhook")
        await self.voteschannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        user_id = data["user"]
        db.register(user_id)
        name = await self.bot.fetch_user(user_id)
        if not name: name = "User"
        else: name = f"{name.mention} (*{name.name}*)"

        db.vote(user_id, "top")
        embed = self.bot.embed(user, "top.gg", f"{name} voted")
        await self.voteschannel.send(embed=embed)

def setup(bot):
    bot.add_cog(Botlists(bot))