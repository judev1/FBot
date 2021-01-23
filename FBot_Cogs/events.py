from discord.ext import commands

class events(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="events", aliases=["event"])
    async def _Events(self, ctx):
        embed = self.bot.fn.embed("FBot Events", self.bot.fn.getevents())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(events(bot))
