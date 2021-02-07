from discord.ext import commands
from functions import cooldown

class say(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="say")
    @commands.check(cooldown)
    async def _Say(self, ctx, *, inp: str):
        await ctx.message.delete()
        await ctx.send(inp + "ㅤ")

    @_Say.error
    async def _SayHandler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == "inp":
                embed = self.bot.fn.errorembed("No Message",
                        "Command usage: 'FBot say <message>'")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(say(bot))
