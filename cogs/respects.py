from discord.ext import commands
import asyncio

F = "🇫"
ongoing_respects = dict()

class respects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="respects")
    async def _Respects(self, ctx, *args):

        text = " ".join(args)

        if text != "":
            msg = await ctx.send(f"React with {F} to pay respects to **{text}**")
            await msg.add_reaction(F)
            ongoing_respects[msg.id] = (text, set())

            await asyncio.sleep(120)

            del ongoing_respects[msg.id]
        else:
            await ctx.reply("You didn't mention paying respects to?")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        msg = reaction.message
        if user.id == self.bot.user.id: return

        if msg.id not in ongoing_respects: return
        if reaction.emoji != F: return

        respects = ongoing_respects[msg.id]
        if user.id in respects[1]: return
        respects[1].add(user.id)
        await msg.channel.send(f"{user.display_name} payed respects to {respects[0]}")

def setup(bot):
    bot.add_cog(respects(bot))