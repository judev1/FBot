import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import sqlite3
import random
import re

conn = sqlite3.connect("ppsize.db")
is_mention = re.compile("<@!?[0-9]{18}>")
ppsize_help = "Command usage: `fbot ppsize` or `fbot ppsize <@mention>`"

class PpsizeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Create blank database if it doesn't already exist
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id integer NOT NULL,
            ppsize integer NOT NULL)""")
        conn.commit()

    @commands.command(name="ppsize")
    async def ppsize(self, ctx, user_mention=None):
        await ctx.trigger_typing()

        member_display_name = None

        if (user_mention is None):
            # `fbot ppsize`
            user_id = ctx.author.id
            member_display_name = ctx.author.display_name
        elif (is_mention.match(user_mention)):
            # `fbot ppsize <@mention>`
            converter = MemberConverter()
            member = await converter.convert(ctx, user_mention)
            user_id = member.id
            member_display_name = member.display_name
        else:
            # `fbot ppsize <something else>`
            await ctx.send(ppsize_help)
            return

        
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT ppsize FROM users WHERE user_id=?", t)
        ppsize = c.fetchone()
        
        if (ppsize is None): # This measures how many elements in ppsize, not the actual ppsize.
            # Make new ppsize and store in database
            ppsize = random.randint(1, 16)
            t = (user_id, ppsize,)
            c.execute("INSERT INTO users VALUES (?, ?)", t)
            conn.commit()
        else:
            # Get ppsize integer from ppsize tuple
            ppsize = ppsize[0]
            
        pp = "8" + "=" * ppsize + "D"
        await ctx.send(f"{member_display_name}'s ppsize: ```{pp}```")

    @commands.command(name="setppsize")
    @commands.is_owner()
    async def setppsize(self, ctx, user_mention, ppsize: int):
        if (user_mention is None):
            await ctx.send("baka")
            return
        else:
            converter = MemberConverter()
            member = await converter.convert(ctx, user_mention)
            user_id = member.id

        c = conn.cursor()
        t = (ppsize, user_id)
        c.execute("""
            UPDATE users SET ppsize=?
            WHERE user_id=?""", t)
        conn.commit()

def setup(bot):
    bot.add_cog(PpsizeCog(bot))
