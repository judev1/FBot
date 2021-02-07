from discord.ext import commands, tasks

class fakeuser: id = 0
user = fakeuser()

class dblcog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fn = bot.fn
        self.dbl = bot.dbl

    @commands.command(name="dbl")
    @commands.is_owner()
    async def _DBL(self, ctx):
        try:
            await self.dbl.post_guild_count()
            embed = self.bot.fn.embed(ctx.author, "Top.gg",
                    f"Updated server count: `{self.dbl.guild_count()}`")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.bot.fn.errorembed("Failed To Update Server Count",
                    f"{type(e).__name__}: {e}")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(dblcog(bot))
