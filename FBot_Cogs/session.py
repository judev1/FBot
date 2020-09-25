import discord
from discord.ext import commands
from functions import fn
from functions import ftime

class session(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="session", aliases=["uptime"])
    async def _Session(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed("FBot's Session", "")
        embed.add_field(name="Session start", value=ftime.getstart())
        embed.add_field(name="Uptime", value=ftime.uptime())
        embed = fn.footer(embed, name, "Uptime")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(session(bot))
