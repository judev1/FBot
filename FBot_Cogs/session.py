from discord.ext import commands

class session(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="session", aliases=["uptime"])
    async def _Session(self, ctx):
        ftime = self.bot.ftime
        embed = self.bot.fn.embed("FBot's Session", "")
        embed.add_field(name="Session start", value=ftime.start)
        embed.add_field(name="Uptime", value=ftime.uptime())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(session(bot))
