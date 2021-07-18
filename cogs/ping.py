from discord.ext import commands

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        ping = (self.bot.latency * 100000) // 100
        embed = self.bot.embed(ctx.author, f"FBots Ping: `{ping}ms`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Ping(bot))