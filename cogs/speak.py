from discord.ext import commands
import lib.database as db

options = ["default", "uwu", "pirate", "biblical", "roadman", "australian", "german", "italian", "safe", "fuck", "triggered", "ironic", "patronise", "confused"]

class Speak(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def speak(self, ctx, arg):
        if arg == "normal": arg = "default"
        if arg in options:
            db.changemode(ctx.guild.id, arg)
            emoji = self.bot.get_emoji(ctx.author.id)
            await ctx.message.add_reaction(emoji)
        else:
            await ctx.reply("That's not a valid mode")

    @commands.command()
    async def devspeak(self, ctx, arg):
        if arg in options:
            db.changemode(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply("That's not a valid mode")

def setup(bot):
    bot.add_cog(Speak(bot))