import discord
from discord.ext import commands
import asyncio

file = open("FBot_Libs/joke.txt")
class JokeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def tell_joke(self, ctx):
        await ctx.send("Ok, I've got a joke.")
        for line in file:
            with ctx.typing():
                sleep_seconds = len(line) / 15 # Typing at 15 chars per second
                await asyncio.sleep(sleep_seconds)
                await ctx.send(line)
                
    
def setup(bot):
    bot.add_cog(JokeCog(bot))
