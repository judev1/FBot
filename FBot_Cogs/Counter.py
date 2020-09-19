"""
Commands (assuming prefix is b!)
b!setcounter/counter/counting) - sets current channel to the 'counting' channel
b!setdevcounter (etc) - same as setcounter but devs can do this on any server
b!number/last - sends current and next number as well as last sender
b!devsetnumber - sets servers number (FOR DEBUGGING), only bot owners can use
b!highscore/hs - displays highscore
"""

import discord
from discord.ext import commands
import sqlite3
import random

conn = sqlite3.connect("counter.db")


class CounterCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Create blank database if it doesn't already exist
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS guilds (
            guild_id integer NOT NULL,
            channel_id integer NOT NULL,
            number integer NOT NULL,
            user_id integer NOT NULL,
            record integer NOT NULL)""")
        conn.commit()

        # Add any servers that are not already in the DB
        c = conn.cursor()
        for guild in self.bot.guilds:
            t = (guild.id,)
            c.execute("SELECT 1 FROM guilds WHERE guild_id=?", t)
            if not c.fetchone():
                c.execute("INSERT INTO guilds VALUES(?, 0, 0, 0, 0)", t)
        conn.commit()

        # Now it's time to get funky
        @self.bot.event
        async def counter(message):
            c = conn.cursor()

            # Ignore channels other than counter channel:
            t = (message.guild.id,)
            c.execute("SELECT channel_id FROM guilds WHERE guild_id=?", t)
            counter_channel_id = c.fetchone()[0]
            if message.channel.id != counter_channel_id:
                return

            # Ignore messages that don't start with a number:
            if not message.content[0].isdigit():
                return

            # Delete any numbers from bots:
            if message.author.bot:
                await message.delete()
                await message.channel.send(
                    "Numbers from bot accounts are not counted.")

            # Ignore bots otherwise:
            if message.author == self.bot.user:
                return

            # Ignore blank messages (e.g attached image with no comment):
            if (message.content == ""):
                return

            # Reset counter if same member does two numbers in a row
            t = (message.guild.id,)
            c.execute("SELECT user_id FROM guilds WHERE guild_id=?", t)
            last_user_id = c.fetchone()[0]

            if (message.author.id == last_user_id):
                t = (message.guild.id,)
                c.execute("""
                    UPDATE guilds SET number=0, user_id=0
                    WHERE guild_id=?""", t)
                conn.commit()
                text = (f"{message.author.mention} ruined it! "
                        "You can't do two numbers in a row.")
                await message.channel.send(text)
                await message.add_reaction("❌")
                return

            # Get guild's current number
            t = (message.guild.id,)
            c.execute("SELECT number FROM guilds WHERE guild_id=?", t)
            guilds_number = int(c.fetchone()[0])

            # Get user's number
            users_number = ""
            for char in message.content:
                if char.isdigit():
                    users_number += char
                else:
                    break
            users_number = int(users_number)

            # Reset counter if number is wrong
            if users_number != guilds_number + 1:
                t = (message.guild.id,)
                c.execute("""
                    UPDATE guilds SET number=0, user_id=0
                    WHERE guild_id=?""", t)
                conn.commit()
                text = (f"{message.author.mention} ruined it!")
                await message.channel.send(text)
                await message.add_reaction("❌")
                return

            # Else, update number + user_id and add confirmation reaction
            else:
                t = (int(users_number), message.author.id, message.guild.id,)
                c.execute("""
                    UPDATE guilds SET number=?, user_id=?
                    WHERE guild_id=?""", t)
                conn.commit()

                await message.add_reaction("✅")

                # If current number is greater than highscore, update highscore
                t = (message.guild.id,)
                c.execute("SELECT record FROM guilds WHERE guild_id=?", t)
                record = c.fetchone()[0]
                if int(users_number) > record:
                    record = users_number
                    t = (record, message.guild.id,)
                    c.execute("""
                        UPDATE guilds SET record=?
                        WHERE guild_id=?""", t)
                    conn.commit()

        self.bot.add_listener(counter, "on_message")

    @commands.command("setcounter", aliases=["counter", "counting"])
    async def set_counter_channel(self, ctx):
        if ctx.author.guild_permissions.administrator:
            c = conn.cursor()
            t = (ctx.channel.id, ctx.guild.id,)
            c.execute("UPDATE guilds SET channel_id=? WHERE guild_id=?", t)
            conn.commit()
            await ctx.send("Set current channel to counting channel")
        else:
            await ctx.send("Only administrators can set the counter channel")

    @commands.command("devsetcounter", aliases=["devcounter", "devcounting"])
    @commands.is_owner()
    async def dev_set_counter_channel(self, ctx):
        c = conn.cursor()
        t = (ctx.channel.id, ctx.guild.id,)
        c.execute("UPDATE guilds SET channel_id=? WHERE guild_id=?", t)
        conn.commit()
        await ctx.send("Set current channel to counting channel")

    @commands.command("number", aliases=["last"])
    async def get_guild_number(self, ctx):
        c = conn.cursor()
        t = (ctx.guild.id,)
        c.execute("SELECT number, user_id FROM guilds WHERE guild_id=?", t)
        row = c.fetchone()
        num, user_id = row[0], row[1]
        last_sender = str(self.bot.get_user(user_id))
        await ctx.send(f"Current number: `{str(num)}` (next is `{str(num+1)}`)"
                       f"\nLast sender is `{str(last_sender)}`")

    @commands.command("highscore", aliases=["hs"])
    async def say_highscore(self, ctx):
        c = conn.cursor()
        t = (ctx.guild.id,)
        c.execute("SELECT record FROM guilds WHERE guild_id=?", t)
        record = str(c.fetchone()[0])
        await ctx.send(f"Guild's highscore is `{record}`")

    @commands.command("devsetnumber")
    @commands.is_owner()
    async def set_number(self, ctx, *, number: str):
        if not number.isdigit():
            await ctx.send("Not a number")
        else:
            c = conn.cursor()
            t = (int(number), ctx.guild.id,)
            c.execute("UPDATE guilds SET number=? WHERE guild_id=? ", t)
            conn.commit()
            await ctx.send("Done")

    @commands.command("highscores", aliases=["countinghighscores", "records"])
    async def say_countinghighscores(self, ctx):
        msg = "Counting highscores:"
        await ctx.trigger_typing()
        c = conn.cursor()
        c.execute("SELECT guild_id, number, record"
                  "FROM guilds ORDER BY record DESC LIMIT 5")
        guild_rank = 0
        for row in c:
            guild_rank += 1
            guild_id, number, record = row
            guild_name = self.bot.get_guild(guild_id).name
            msg += (f"\n{guild_rank}. {guild_name},"
                    "Guild highscore: {record}, Current number: {number}")
        await ctx.send(msg)


def setup(bot):
    bot.add_cog(CounterCog(bot))


def teardown(bot):
    self.bot.remove_listener(counter, "on_message")
    conn.close()
