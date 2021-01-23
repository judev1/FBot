from discord.ext import commands

class notices(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="notices", aliases=["notice"])
    async def _Notices(self, ctx):
        notices = self.bot.fn.getnotices()
        embed = self.bot.fn.embed("FBot Notices", notices)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(notices(bot))
