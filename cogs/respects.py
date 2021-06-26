from discord.ext import commands
from discord import AllowedMentions
from lib.modes import *

F = "🇫"
ongoing_respects = dict()

class respects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="respects")
    async def _Respects(self, ctx):

        reference = ctx.message.reference
        if reference:
            message = await ctx.fetch_message(id=reference.message_id)
            text = message.content
        else:
            text = ctx.message.content
            prefix = len(self.bot.fn.getprefix(self.bot, ctx.message))
            text = text[prefix + 9:]

        if text:
            text = capitalise(sanitise_text(text))
            message = await ctx.send(f"React with {F} to pay respects to **{text}**")
            await message.add_reaction(F)
            ongoing_respects[message.id] = (text, set())
        else:
            await ctx.reply("You didn't include or reference anything to pay respects to!")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        message = reaction.message
        channel = message.channel
        if user.bot: return

        if reaction.emoji != F: return

        if message.id not in ongoing_respects: return
        respects = ongoing_respects[message.id]
        if user.id in respects[1]: return

        respects[1].add(user.id)
        await channel.send(f"{user.mention} payed respects to **{respects[0]}**", allowed_mentions=AllowedMentions.none())

def setup(bot):
    bot.add_cog(respects(bot))