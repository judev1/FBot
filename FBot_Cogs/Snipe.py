import discord
from discord.ext import commands

snipes = dict()

class SnipeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild:
            snipes[message.guild.id] = message

    @commands.command(name='snipe')
    @commands.is_owner()
    async def do_snipe(self, ctx):
        try:
            msg = ("Sniped message\n"
                f"Sender: {snipes[ctx.guild.id].author.display_name}\n"
                f"Message: {snipes[ctx.guild.id].content}")
            await ctx.send(msg)
        except KeyError:
            await ctx.send("No recently deleted messages to snipe")


def setup(bot):
    bot.add_cog(SnipeCog(bot))
