import discord
from discord.ext import commands
from Functions import Functions as fn
from Functions import Time as ftime

ver, fboturl, variables = fn.Get_Vars()
sessionstart = ftime.Get_Start()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="session", aliases=["uptime"])
    async def _Session(self, ctx):
        name = ctx.author.display_name
        
        embed = discord.Embed(title="FBot's session", colour=0xF42F42)
        embed.add_field(name="Session start", value=sessionstart)
        embed.add_field(name="Uptime", value=ftime.Uptime())
        embed.set_footer(text=f"Uptime requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
