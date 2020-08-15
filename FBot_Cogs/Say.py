import discord
from discord.ext import commands

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="say")
    async def _Say(self, ctx, *message):
        message = " ".join(message)
        if len(message) == 0:
            embed = discord.Embed(title="**Error:** `No Message`", description=f"```Usage: 'FBot say <message>'```", colour=0xF42F42)
            await send(embed=embed)
        else:
            await ctx.message.delete()
            await ctx.send(message)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
