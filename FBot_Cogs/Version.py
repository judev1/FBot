import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars(var1="lastupdated")
lastupdated = variables[0]

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="version", aliases=["ver"])
    async def _Version(self, ctx):
        name = ctx.author.display_name
        
        embed = discord.Embed(title=f"FBots Version", colour=0xF42F42)
        embed.add_field(name="Version", value=ver)
        embed.add_field(name="Released", value=lastupdated)
        embed.set_footer(text=f"Version requested by {name}", icon_url=fboturl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
