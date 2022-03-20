from discord import AllowedMentions
from discord import app_commands
from discord import Interaction
from lib import modes

class Modes:
    normal = str
    uwu = modes.uwu
    pirate = modes.pirate
    biblical = modes.biblical
    roadman = modes.roadman
    aussie = modes.australian
    german = modes.german
    italian = modes.italian
    safe = modes.safe
    fuck = modes.fuck
    triggered = modes.triggered
    ironic = modes.ironic
    patronise = modes.patronise
    confused = modes.confused

class Say(app_commands.Group):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command()
    async def say(self, interaction: Interaction, filter: Modes, *, text):
        text = " ".join(text)
        channel = interaction.channel
        if text:
            text = filter(modes.sanitise_text(text))
            if len(text) <= 4000:
                await channel.send(text, allowed_mentions=AllowedMentions.none())
            else:
                text = "Text is too long to send"
                if filter:
                    text = filter(text)
                await channel.send_message(text)
        else:
            text = "You didn't include or reference any text to say!"
            if filter:
                text = filter(text)
            await channel.reply(text)

def setup(bot):
    bot.tree.add_command(Say())

# class Say(commands.Cog):

#     def __init__(self, bot):
#         self.bot = bot

#     async def send(self, ctx, filter=None, delete=False):

#         reference = ctx.message.reference
#         if reference:
#             message = await ctx.fetch_message(id=reference.message_id)
#             text = message.content
#         else:
#             text = ctx.message.content
#             prefix = fn.getprefix(self.bot, ctx.message)
#             command = ctx.command.name
#             if not text.lower().startswith(prefix + command):
#                 for alias in ctx.command.aliases:
#                     if text.lower().startswith(prefix + alias):
#                         command = alias
#                         break
#             text = text[len(prefix) + len(command) + 1:]

#         if text:
#             if filter:
#                 text = sanitise_text(text)
#                 text = filter(text)

#             try:
#                 await ctx.send(text, allowed_mentions=AllowedMentions.none())
#             except:
#                 text = "Text is too long to send"
#                 if filter:
#                     text = filter(text)
#                 await ctx.send(text)
#         else:
#             text = "You didn't include or reference any text to say!"
#             if filter:
#                 text = filter(text)
#             await ctx.reply(text)

#     @commands.command()
#     async def say(self, ctx):
#         await self.send(ctx, delete=True)

#     @commands.command()
#     async def uwu(self, ctx):
#         await self.send(ctx, filter=uwu)

#     @commands.command()
#     async def pirate(self, ctx):
#         await self.send(ctx, filter=pirate)

#     @commands.command()
#     async def biblical(self, ctx):
#         await self.send(ctx, filter=biblical)

#     @commands.command()
#     async def roadman(self, ctx):
#         await self.send(ctx, filter=roadman)

#     @commands.command(aliases=["aussie"])
#     async def australian(self, ctx):
#         await self.send(ctx, filter=australian)

#     @commands.command(aliases=["deutch"])
#     async def german(self, ctx):
#         await self.send(ctx, filter=german)

#     @commands.command()
#     async def italian(self, ctx):
#         await self.send(ctx, filter=italian)

#     @commands.command()
#     async def safe(self, ctx):
#         await self.send(ctx, filter=safe)

#     @commands.command()
#     async def fuck(self, ctx):
#         await self.send(ctx, filter=fuck)

#     @commands.command()
#     async def triggered(self, ctx):
#         await self.send(ctx, filter=triggered)

#     @commands.command()
#     async def ironic(self, ctx):
#         await self.send(ctx, filter=ironic)

#     @commands.command()
#     async def patronise(self, ctx):
#         await self.send(ctx, filter=patronise)

#     @commands.command()
#     async def confused(self, ctx):
#         await self.send(ctx, filter=confused)

# def setup(bot):
#     bot.add_cog(Say(bot))