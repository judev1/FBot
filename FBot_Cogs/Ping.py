import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="ping")
    async def _Ping(self, ctx):
        name = ctx.author.display_name
        
        embed = discord.Embed(title=f"FBots Ping: `{round((self.bot.latency * 100000) / 100)}ms`", colour=0xF42F42)
        embed.set_footer(text=f"Ping requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)
          
def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
