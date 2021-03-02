from discord.ext import commands
from functions import predicate
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

class fball(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        @self.bot.event
        async def _FBall(message):
            content = message.content.lower()
            if content.startswith("fball ") or content.startswith("8ball "):
                await message.channel.send(choice(responses))
        self.bot.add_listener(_FBall, "on_message")

    @commands.command(name="fball")
    @commands.check(predicate)
    async def _FBot_FBall(self, ctx):
        await ctx.send(choice(responses))

def setup(bot):
    bot.add_cog(fball(bot))

def teardown(bot):
    self.bot.remove_listener(fball, "on_message")
