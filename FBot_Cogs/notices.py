from discord.ext import commands
from functions import fn

class notices(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="notices", aliases=["notice"])
    async def _Notices(self, ctx):
        name = ctx.author.display_name
        notices = fn.getnotices()
        embed = fn.embed("FBot Notices", notices)
        embed= fn.footer(embed, name, "Notices")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(notices(bot))
