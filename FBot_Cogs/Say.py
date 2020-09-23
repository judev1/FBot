import discord
from discord.ext import commands
from functions import fn

class say(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="say")
    async def do_repeat(self, ctx, *, inp: str):
        await ctx.message.delete()
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "inp":
                embed = fn.errorembed("No Message",
                                      "Usage: 'FBot say <message>'")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(say(bot))
