from discord.ext import commands, tasks
import dbl

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
        embed = self.bot.fn.embed(ctx.author, "Loading...")
        msg = await ctx.send(embed=embed)
        try:
            await self.dbl.post_guild_count()
        except: pass
        try:
            embed = self.bot.fn.embed(ctx.author, "Top.gg",
                    f"Updated server count: `{self.dbl.guild_count()}`")
            await msg.edit(embed=embed)
        except:
            embed = self.bot.fn.embed(ctx.author, "Failed")
            await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(dblcog(bot))
