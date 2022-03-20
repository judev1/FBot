from discord.ext import commands
from random import choice
import asyncio
import os

jokes = list()
for joke in os.listdir("data/Jokes"):
    with open("data/Jokes/" + joke, "r") as file:
        jokes.append(file.read().split("\n"))
active_channels = set()

class Joke(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):

        if (ctx.channel.id in active_channels):
            await ctx.reply("I'm already telling a joke, do `fbot shutup` to cancel")
            return

        await ctx.reply("Ok, I've got a joke.\nDo `fbot shutup` to cancel")

        active_channels.add(ctx.channel.id)
        the_joke = choice(jokes)

        for line in the_joke:
            async with ctx.channel.typing():
                for i in range(0, len(line)):
                    sleep_seconds = 1 / 15
                    await asyncio.sleep(sleep_seconds)
                    if (not ctx.channel.id in active_channels):
                        return
                await ctx.send(line)

        active_channels.remove(ctx.channel.id)

    @commands.command()
    async def shutup(self, ctx):
        if (ctx.channel.id in active_channels):
            active_channels.remove(ctx.channel.id)
            await ctx.reply("Ok, but I was just getting to the best part")
        else:
            await ctx.reply("You wish")

    @commands.command()
    async def jokeinfo(self, ctx):
        await ctx.reply("Active channels: " + str(active_channels))

def setup(bot):
    bot.add_cog(Joke(bot))
