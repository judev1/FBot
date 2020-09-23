from discord.ext import commands
from functions import fn

class version(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="version", aliases=["ver"])
    async def _Version(self, ctx):
        name = ctx.author.display_name
        
        embed = fn.embed("FBots Version", "")
        embed.add_field(name="Version", value=fn.getinfo("ver"))
        embed.add_field(name="Released", value=fn.getinfo("lastupdated"))
        embed = fn.footer(embed, name, "Version")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(version(bot))
