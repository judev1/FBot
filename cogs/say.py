from discord import AllowedMentions
from discord.ext import commands
from lib.modes import *

class say(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def say(self, ctx, text, filter=None, delete=False):

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
    async def _Say(self, ctx, *, text):
        await self.say(ctx, text, delete=True)

    @commands.command(name="uwu")
    async def _UWU(self, ctx, *, text):
        await self.say(ctx, text, filter=uwu)

    @commands.command(name="confused")
    async def _Confused(self, ctx, *, text):
        await self.say(ctx, text, filter=confused)

    @commands.command(name="pirate")
    async def _Pirate(self, ctx, *, text):
        await self.say(ctx, text, filter=pirate)

    @commands.command(name="triggered")
    async def _Triggered(self, ctx, *, text):
        await self.say(ctx, text, filter=triggered)

    @commands.command(name="italian")
    async def _Italian(self, ctx, *, text):
        await self.say(ctx, text, filter=italian)

    @commands.command(name="fuck")
    async def _Fuck(self, ctx, *, text):
        await self.say(ctx, text, filter=fuck)

    @commands.command(name="ironic")
    async def _Ironic(self, ctx, *, text):
        await self.say(ctx, text, filter=ironic)

    @commands.command(name="patronise")
    async def _Patronise(self, ctx, *, text):
        await self.say(ctx, text, filter=patronise)

    @commands.command(name="colonial")
    async def _Colonial(self, ctx, *, text):
        await self.say(ctx, text, filter=colonial)

    @commands.command(name="safe")
    async def _Safe(self, ctx, *, text):
        await self.say(ctx, text, filter=safe)

    @commands.command(name="biblical")
    async def _Biblical(self, ctx, *, text):
        await self.say(ctx, text, filter=biblical)

def setup(bot):
    bot.add_cog(say(bot))