from discord.ext.commands import MemberConverter
from discord import AllowedMentions
from discord.ext import commands
import sqlite3
import random
import re

is_mention = re.compile("<@!?[0-9]{18}>")
ppsize_help = "Command usage: `fbot ppsize` or `fbot ppsize <@mention>`"

class ppsize(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ppsize")
    async def ppsize(self, ctx, user_mention=None):
        async with ctx.channel.typing():
            if (user_mention is None):
                # No user mention defaults to sender
                member = ctx.author
            elif (is_mention.match(user_mention)):
                converter = MemberConverter()
                member = await converter.convert(ctx, user_mention)
            else:
                # `user_mention` is not member, send command help
                member = None
                message = ppsize_help

            if (member is not None):
                ppsize = None

                if member.bot:
                    message = "Bots don't have pps, you do know that?"
                else:
                    try:
                        ppsize = self.bot.db.getppsize(member.id)
                        if ppsize < 0:
                            ppsize = random.randint(0, 16)
                            self.bot.db.updateppsize(member.id, ppsize)
                    except:
                        # Register user and give them a ppsize
                        self.bot.db.register(member.id)
                        ppsize = random.randint(0, 16)
                        self.bot.db.updateppsize(member.id, ppsize)
                            
                    if (ppsize is not None):
                        pp = "8" + "=" * ppsize + "D"
                        message = f"{member.mention}'s ppsize: `{pp}`"
        await ctx.send(message, allowed_mentions=AllowedMentions.all())

             

    @commands.command(name="devsetppsize")
    @commands.is_owner()
    async def setppsize(self, ctx, user_mention, ppsize: int):
        if (ppsize > 1950):
            await ctx.send("Too big: ppsize exceeds max message length")
        elif (user_mention is None):
            await ctx.send("baka")
        else:
            converter = MemberConverter()
            member = await converter.convert(ctx, user_mention)
            user_id = member.id

            self.bot.db.updateppsize(user_id, ppsize)

def setup(bot):
    bot.add_cog(ppsize(bot))