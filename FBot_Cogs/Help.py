import discord
import functions
from discord.ext import commands
from functions import fn

class help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="help", aliases=["?"])
    async def _Help(self, ctx):
        name = ctx.message.author.display_name
        
        embed = fn.embed(
"FBot Help",

"**Useful Commands**\n"
"Use `FBot on/off` to toggle fbot\n"
"Use `FBot cmds` for a list of commands\n\n"

"**Useful Links**\n"
f"[Our Top.gg page]({functions.topggurl}) and "
f"[Join our server!]({functions.serverurl})\n\n"

"**You can help FBot too!**\n"
f"[Vote here!]({functions.voteurl})"
)
        embed = fn.footer(embed, name, "Help")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))