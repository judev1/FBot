import discord
from discord.ext import commands
from collections import deque # deque = queue datatype
import os
import io

snipes = dict()
max_snipes = 10 # max snipes per channel

class snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild: return
        if message.channel.id not in snipes:
            
            snipes[message.channel.id] = deque(maxlen=max_snipes)
        snipes[message.channel.id].appendleft((message, "Deleted message"))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content: return
        if not before.guild: return
        # message = before
        
        if before.channel.id not in snipes:
            snipes[before.channel.id] = deque(maxlen=max_snipes)
        snipes[before.channel.id].appendleft((before, "Edited message"))

    @commands.command(name="snipe")
    async def do_snipe(self, ctx, number=1):
        if ctx.message.channel.id not in snipes:
            embed = self.bot.fn.embed("FBot Snipe",
                    "```No recently deleted/edited messages to snipe```")
            await ctx.send(embed=embed)
            return
        
        if number < 1 or number > 10:
            await ctx.send("`Number of snipes must be between 1 and 10`")
            return

        msg = ""
        if number > len(snipes[ctx.channel.id]):
            msg += "Showing all available snipes from this channel\n"
            number = len(snipes[ctx.channel.id])
        if number > 1:
            msg += "Snipes are in order of most recent snipes descending\n"
        for i in range(number):
            snipe = snipes[ctx.channel.id][i]
            # snipe[0] is the message object
            # snipe[1] is the string "Deleted" or "Edited"
            member = snipe[0].author
            msg += f"""Sender: `{member.display_name}` (`{member}`)
{snipe[1]}:
{snipe[0].content}\n"""
            if len(snipe[0].content) == 0:
                msg += "`(If message is blank, it may have been an image, join message or pin)`\n"

            msg += "\n"  # one more newline for good luck
        if len(msg) > 1900:  # 2048 char limit minus embed overhead
            with io.open("fbot_snipe.txt", "w+", encoding="utf8") as file:
                file.write(msg)
            await ctx.send(
                "`Sniped messages were longer than 2000 chars, sending as file:`",
                file=discord.File(r"fbot_snipe.txt"))
            os.remove("fbot_snipe.txt")
        else:
            embed = self.bot.fn.embed("FBot snipe", msg)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(snipe(bot))
