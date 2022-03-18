from discord.ext import commands
import discord

class Users(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, user: discord.User=None):
        await ctx.reply("This command is being reworked. Stay updated by clicking the link in the next embed!")
        await ctx.invoke(self.bot.get_command("server"))

def setup(bot):
    bot.add_cog(Users(bot))