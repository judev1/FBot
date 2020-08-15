import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars(var1="topggurl", var2="serverurl", var3="voteurl")
topggurl = variables[0]
serverurl = variables[1]
voteurl = variables[2]

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="help", aliases=["?"])
    async def _Help(self, ctx):
        name = ctx.message.author.display_name
        
        embed = discord.Embed(title="FBot Help", description="**Useful Commands**\n"
                                                             "Use `FBot on/off` to toggle fbot\n"
                                                             "Use `FBot cmds` for a list of commands\n\n"
                                                             "**Useful Links**\n"
                                                             f"[Our Top.gg page]({topggurl}) and "
                                                             f"[Join our server!]({serverurl})\n\n"
                                                             "**You can help FBot too!**\n"
                                                             f"[Vote here!]({voteurl})", colour=0xF42F42)
        embed.set_footer(text=f"Help requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
