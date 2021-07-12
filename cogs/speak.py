from discord.ext import commands
import lib.database as db

options = ["default", "uwu", "confused", "pirate", "triggered", "italian", "fuck", "ironic", "patronise", "colonial", "safe", "biblical"]

class speak(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="speak")
    async def _Speak(self, ctx, arg):
        if arg == "normal": arg = "default"
        if arg in options:
            db.changemode(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply("That's not a valid mode")

    @commands.command(name="devspeak")
    @commands.is_owner()
    async def _DevSpeak(self, ctx, arg):
        if arg in options:
            db.changemode(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply("That's not a valid mode")

def setup(bot):
    bot.add_cog(speak(bot))