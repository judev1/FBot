import discord
from discord.ext import commands
import random as random

responses = ["yeah", "nah", "maybe", "idk"]

class FballCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fball", aliases=["8ball"])
    async def do_fball(self, ctx):
        response = random.choice(responses)
        await ctx.send(response)

def setup(bot):
    bot.add_cog(FballCog(bot))
