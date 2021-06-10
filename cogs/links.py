from discord.ext import commands

class links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def _Invite(self, ctx):
        fn = self.bot.fn
        embed = fn.embed(ctx.author, "Invite FBot to your server!", url=fn.invite)
        await ctx.send(embed=embed)

    @commands.command(name="server")
    async def _Server(self, ctx):
        fn = self.bot.fn
        embed = fn.embed(ctx.author, "Join our server, it's for support and fun!", url=fn.server)
        await ctx.send(embed=embed)

    @commands.command(name="links")
    async def _Links(self, ctx):

        fn = self.bot.fn
        embed = fn.embed(ctx.author, "FBot links",)

        embed.add_field(name=":closed_book: **__GENERAL LINKS__**", inline=False, value="The standard discord links for FBot")
        embed.add_field(name="Invite FBot", value=f"[Click here]({fn.invite})")
        embed.add_field(name="Support Server", value=f"[Click here]({fn.server})")

        embed.add_field(name=":green_book: **__EXTERNAL LINKS__**", inline=False, value="Other non-discord FBot affliated sites")
        embed.add_field(name="Our Patreon", value=f"[Click here]({fn.patreon})")
        embed.add_field(name="Our Website", value=f"[Click here]({fn.site})")
        embed.add_field(name="Our Github", value=f"[Click here]({fn.github})")

        embed.add_field(name=":blue_book: **__BOT LISTS__**", inline=False, value="All the bot lists which FBot is shown on")
        embed.add_field(name="discordbotlist.com", value=f"[Click here]({fn.dbl})")
        embed.add_field(name="top.gg", value=f"[Click here]({fn.top})")
        embed.add_field(name="listcord.gg", value=f"[Click here]({fn.ligg})")
        embed.add_field(name="botsfordiscord.com", value=f"[Click here]({fn.bfd})")
        embed.add_field(name="botlist.me", value=f"[Click here]({fn.blme})")
        embed.add_field(name="botlist.space", value=f"[Click here]({fn.blsp})")
        embed.add_field(name="discord-botlist.eu", value=f"[Click here]({fn.dbeu})")
        embed.add_field(name="discord.bots.gg", value=f"[Click here]({fn.dbgg})")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(links(bot))