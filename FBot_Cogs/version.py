from discord.ext import commands
from functions import predicate

class version(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ver")
    @commands.check(predicate)
    async def _Version(self, ctx):
        fn = self.bot.fn
        ver, updated = fn.getinfo("ver"), fn.getinfo("lastupdated")
        embed = fn.embed(ctx.author, "FBot's Version")
        embed.add_field(name="Version", value=f"`{ver}`")
        embed.add_field(name="Released", value=f"`{updated}`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(version(bot))
