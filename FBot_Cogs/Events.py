import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="events", aliases=["event"])
    async def _Events(self, ctx):
        name = ctx.message.author.display_name
        events = fn.Get_Events()
        
        embed = discord.Embed(title="FBot Events", description=events, colour=0xF42F42)
        embed.set_footer(text=f"Events requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
