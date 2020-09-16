import discord
from discord.ext import commands
import asyncio

file = open("FBot_Libs/joke.txt")

active_channels = set()
active_guilds = set()

class JokeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="joke")
    async def tell_joke(self, ctx):
        
        if ctx.channel.id in active_channels:
            await ctx.send("I'm already telling a joke, do `fbot shutup` to cancel")
            return
        
        if ctx.guild.id in active_guilds:
            ctx.send("I'm already telling a joke in another channel, do `fbot shutup` to cancel")
            return

        await ctx.send("Ok, I've got a joke.\nDo `fbot shutup` to cancel")
        
        active_channels.add(ctx.channel.id)
        active_guilds.add(ctx.guild.id)
        
        for line in file:
            await ctx.trigger_typing()
            sleep_seconds = len(line) / 15 # Typing at 15 chars per second
            await asyncio.sleep(sleep_seconds)
            if (not ctx.channel.id in active_channels):
                return
            await ctx.send(line)

        # Joke is finished, so we remove it from active channels/guilds
        active_channels.remove(ctx.channel.id)
        active_guilds.remove(ctx.guild.id)
                
    @commands.command(name="shutup")
    async def stop_joke(self, ctx):
        if (ctx.channel.id in active_channels):
            active_channels.remove(ctx.channel.id)
            await ctx.send("Ok, but I was just getting to the best part.")            
        if (ctx.guild.id in active_guilds):
            active_guilds.remove(ctx.guild.id)
        

    @commands.command(name="jokeinfo")
    @commands.is_owner()
    async def say_jokeinfo(self, ctx):
        await ctx.send("Active channels: " + str(active_channels) + "\n\nActive guilds: " + str(active_guilds))
        
    
def setup(bot):
    bot.add_cog(JokeCog(bot))
