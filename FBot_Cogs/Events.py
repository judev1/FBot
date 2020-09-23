import discord
from discord.ext import commands
from functions import fn

class events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="events", aliases=["event"])
    async def _Events(self, ctx):
        name = ctx.message.author.display_name
        embed = fn.embed("FBot Events", fn.getevents())
        embed = fn.footer(embed, name, "Events")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(events(bot))
