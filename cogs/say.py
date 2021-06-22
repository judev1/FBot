from discord import AllowedMentions
from discord.ext import commands
from lib.modes import *

class say(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def say(self, ctx, filter=None, delete=False):

        reference = ctx.message.reference
        if reference:
            message = await ctx.fetch_message(id=reference.message_id)
            text = message.content
        else:
            text = ctx.message.content
            prefix = len(self.bot, ctx.message)
            command = len(ctx.message.command)
            text = text[prefix + command + 1:]

        if not text:
            text = "You didn't include or reference any text!"
            if filter:
                text = filter(text)
                text = capitalise(text)
            await ctx.send(text)

        if filter:
            text = sanitise_text(text)
            text = filter(text)
        text = capitalise(text)

        try:
            await ctx.send(text, allowed_mentions=AllowedMentions.none())
        except:
            text = "Text is too long to send"
            if filter:
                text = filter(text)
                text = capitalise(text)
            await ctx.send(text)

    @commands.command(name="say")
    async def _Say(self, ctx):
        await self.say(ctx, delete=True)

    @commands.command(name="uwu")
    async def _UWU(self, ctx):
        await self.say(ctx, filter=uwu)

    @commands.command(name="confused")
    async def _Confused(self, ctx):
        await self.say(ctx, filter=confused)

    @commands.command(name="pirate")
    async def _Pirate(self, ctx):
        await self.say(ctx, filter=pirate)

    @commands.command(name="triggered")
    async def _Triggered(self, ctx):
        await self.say(ctx, filter=triggered)

    @commands.command(name="italian")
    async def _Italian(self, ctx):
        await self.say(ctx, filter=italian)

    @commands.command(name="fuck")
    async def _Fuck(self, ctx):
        await self.say(ctx, filter=fuck)

    @commands.command(name="ironic")
    async def _Ironic(self, ctx):
        await self.say(ctx, filter=ironic)

    @commands.command(name="patronise")
    async def _Patronise(self, ctx):
        await self.say(ctx, filter=patronise)

    @commands.command(name="colonial")
    async def _Colonial(self, ctx):
        await self.say(ctx, filter=colonial)

    @commands.command(name="safe")
    async def _Safe(self, ctx):
        await self.say(ctx, filter=safe)

    @commands.command(name="biblical")
    async def _Biblical(self, ctx):
        await self.say(ctx, filter=biblical)

def setup(bot):
    bot.add_cog(say(bot))