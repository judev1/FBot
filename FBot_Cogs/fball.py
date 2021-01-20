import discord
from discord.ext import commands
import random as random

responses = ["Without a doubt... yes.",
             "Without a doubt... no.",
             "Perhaps.",
             "...Isn't it obvious?",
             "You don't want to know.",
             "HAHAHAHAHAHA no",
             "I'd be lying if I said yes."
             "yep"]

class fball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fball", aliases=["8ball"])
    async def do_fball(self, ctx):
        response = random.choice(responses)
        await ctx.send(response)

def setup(bot):
    bot.add_cog(fball(bot))
