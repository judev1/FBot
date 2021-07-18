from discord import AllowedMentions
from discord.ext import commands
import lib.functions as fn
from lib.modes import *

class Say(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def send(self, ctx, filter=None, delete=False):

        reference = ctx.message.reference
        if reference:
            message = await ctx.fetch_message(id=reference.message_id)
            text = message.content
        else:
            text = ctx.message.content
            prefix = len(fn.getprefix(self.bot, ctx.message))
            command = len(ctx.command.name)
            text = text[prefix + command + 1:]

        if text:
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
        else:
            text = "You didn't include or reference any text to say!"
            if filter:
                text = filter(text)
                text = capitalise(text)
            await ctx.reply(text)

    @commands.command()
    async def say(self, ctx):
        await self.send(ctx, delete=True)

    @commands.command()
    async def uwu(self, ctx):
        await self.send(ctx, filter=uwu)

    @commands.command()
    async def confused(self, ctx):
        await self.send(ctx, filter=confused)

    @commands.command()
    async def pirate(self, ctx):
        await self.send(ctx, filter=pirate)

    @commands.command()
    async def triggered(self, ctx):
        await self.send(ctx, filter=triggered)

    @commands.command()
    async def italian(self, ctx):
        await self.send(ctx, filter=italian)

    @commands.command()
    async def fuck(self, ctx):
        await self.send(ctx, filter=fuck)

    @commands.command()
    async def ironic(self, ctx):
        await self.send(ctx, filter=ironic)

    @commands.command()
    async def patronise(self, ctx):
        await self.send(ctx, filter=patronise)

    @commands.command()
    async def colonial(self, ctx):
        await self.send(ctx, filter=colonial)

    @commands.command()
    async def safe(self, ctx):
        await self.send(ctx, filter=safe)

    @commands.command()
    async def biblical(self, ctx):
        await self.send(ctx, filter=biblical)

def setup(bot):
    bot.add_cog(Say(bot))