from discord.ext import commands
from functions import fn

class ping(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ping")
    async def _Ping(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed(f"FBots Ping: `{round((self.bot.latency * 100000) / 100)}ms`", "")
        embed = fn.footer(embed, name, "Ping")
        await ctx.send(embed=embed)
          
def setup(bot):
    bot.add_cog(ping(bot))