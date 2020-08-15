import discord
from discord.ext import commands
from Functions import Functions as fn
from Functions import Time as ftime

ver, fboturl, variables = fn.Get_Vars(var="lastupdated")
lastupdated = variables[0]
sessionstart = ftime.Get_Start()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="infomation", aliases=["info"])
    async def _Info(self, ctx):

        totalmembers = 0
        for servers in self.bot.guilds:
            if str(servers.id) != "264445053596991498":
                totalmembers += servers.member_count

        embed = discord.Embed(title="FBot Info", colour=0xF42F42)
        embed.add_field(name="Session start", value=sessionstart)
        embed.add_field(name="Servers", value=len(self.bot.guilds) - 1)
        embed.add_field(name="Last Updated", value=lastupdated)
        embed.add_field(name="Uptime", value=ftime.Uptime())
        embed.add_field(name="Members", value=totalmembers)
        embed.add_field(name="Version", value=ver)
        embed.set_footer(text="Created by justjude#2296 & LinesGuy#9260", icon_url=fboturl)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
