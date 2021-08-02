from discord.ext.commands import MemberConverter
from discord import AllowedMentions
from discord.ext import commands
import lib.database as db
import random
import re

is_mention = re.compile("<@!?[0-9]{18}>")

class PPSize(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ppsize(self, ctx, user_mention=None):
        async with ctx.channel.typing():
            if (user_mention is None):
                member = ctx.author
            elif (is_mention.match(user_mention)):
                converter = MemberConverter()
                member = await converter.convert(ctx, user_mention)
            else:
                member = None
                text = "Command usage: `fbot ppsize` or `fbot ppsize <@mention>`"

            if (member is not None):
                ppsize = None

                if member.bot:
                    text = "Bots don't have pps, you do know that?"
                else:
                    try:
                        ppsize = db.getppsize(member.id)
                        if ppsize < 0:
                            ppsize = random.randint(0, 16)
                            db.updateppsize(member.id, ppsize)
                    except:
                        db.register(member.id)
                        ppsize = random.randint(0, 16)
                        db.updateppsize(member.id, ppsize)

                    if (ppsize is not None):
                        pp = "8" + "=" * ppsize + "D"
                        text = f"{member.mention}'s ppsize: `{pp}`"
        await ctx.send(text, allowed_mentions=AllowedMentions.all())

    @commands.command()
    async def setppsize(self, ctx, user_mention, ppsize: int):
        if (ppsize > 1950):
            await ctx.reply("Too big: ppsize exceeds max message length")
        elif (user_mention is None):
            await ctx.reply("baka")
        else:
            converter = MemberConverter()
            member = await converter.convert(ctx, user_mention)
            user_id = member.id

            db.updateppsize(user_id, ppsize)

def setup(bot):
    bot.add_cog(PPSize(bot))