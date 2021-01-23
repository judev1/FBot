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
                member = ctx.author
                member_mention = member.mention
                print("No mention:", [member_mention], type(member_mention))
            elif (is_mention.match(user_mention)):
                converter = MemberConverter()
                member = await converter.convert(ctx, user_mention)
                member_mention = member.mention
                print("mention:", [member_mention], type(member_mention))
            else:
                await ctx.send(ppsize_help)
                return
            
            try:
                ppsize = self.bot.db.getppsize(member.id)
            except:
                if member.bot:
                    await ctx.send("Bot don't have pps, you know that")
                    return
                else:
                    self.bot.db.register(member.id)
                    ppsize = self.bot.db.getppsize(member.id)

            if ppsize == -1:
                ppsize = random.randint(0, 16)
                self.bot.db.updateppsize(member.id, ppsize)
            pp = "8" + "=" * ppsize + "D"
            await ctx.send(f"{user_mention}'s ppsize: `{pp}`",
                  allowed_mentions=AllowedMentions.all())
            return
            

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
