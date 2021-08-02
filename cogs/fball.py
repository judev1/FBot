from discord.ext import commands
from random import choice

responses = ["Without a doubt... yes.",
             "Without a doubt... no.",
             "In my professional opinion: nah.",
             "In my professional opinion: yup.",
             "In my professional opinion: probs.",
             "If I had to guess I'd say yes.",
             "If I had to guess I'd say no.",
             "If I had to guess I'd say maybe.",
             "yep",
             "NOT AT ALL! oh wait, actually yes",
             "I'll say yes if you shut up",
             "Most definitely not.",
             "HAHAHAHAHAHA no.",
             "I think so, mm, maybe not",
             "I'd be lying if I said yes.",
             "Perhaps.",
             "I'll think about it",
             "...Isn't it obvious?",
             "You don't want to know.",
             "Are you for real?",
             "Sensible questions only.",
             "What are you asking me for?",
             "Who knows! I don't!",
             "m y  s e r v i c e s  a r e n ' t  f r e e  y e  k n o w"]

class FBall(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.bot.ready():
            return

        content = message.content.lower()
        if content.startswith("fball "):
            await message.reply(choice(responses))

    @commands.command()
    async def fball(self, ctx):
        await ctx.reply(choice(responses))

def setup(bot):
    bot.add_cog(FBall(bot))