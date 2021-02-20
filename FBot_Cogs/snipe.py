from discord import AuditLogAction
from discord.ext import commands
from functions import cooldown
from collections import deque
import discord
import os
import io

snipes = dict()
max_snipes = 10 # max snipes per channel
message_delete = AuditLogAction.message_delete

class snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="snipe")
    @commands.check(cooldown)
    async def _Snipe(self, ctx, number=10):
        user = ctx.author
        if ctx.message.channel.id not in snipes:
            embed = self.bot.fn.embed(user, "FBot Snipe",
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

        i = 0
        for snipe in snipes[ctx.channel.id]:

            action = snipe["action"]
            sender = snipe["sender"]
            time = snipe["time"]
            if action == "edited":
                message = snipe["message"]
                msg += f"\n{sender} edited their [message]({message}) at `{time}`"
            elif action == "deleted":
                deleter = snipe["deleter"]
                msg += f"\n{deleter} deleted {sender}'s message at `{time}`"

            content = snipe["content"]
            if content == "":
                content = "`message's contents are unreadable`"
            msg += "\n" + content + "\n"

            i += 1
            if i == number: break

        if len(msg) > 1900:  # 2048 char limit minus embed overhead
            with io.open("fbot_snipe.txt", "w+", encoding="utf8") as file:
                file.write(msg)
            await ctx.send(
                "`Sniped messages were longer than 2000 chars, sending as file:`",
                file=discord.File(r"fbot_snipe.txt"))
            os.remove("fbot_snipe.txt")
        else:
            embed = self.bot.fn.embed(user, "FBot snipe", msg)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.guild: return

        prefix = self.bot.fn.getprefix(self.bot, message)
        commandcheck = message.content[len(prefix):]
        if commandcheck.startswith("say "):
            if not message.author.bot:
                bot_id = self.bot.user.id
                if  message.channel.permissions_for(
                    message.guild.get_member(bot_id)).send_messages:
                    return
        deleter = "User"
        try:
            async for deleted in message.guild.audit_logs(limit=1,
                                 oldest_first=False, action=message_delete):
                deleter = deleted.user.mention
        except: pass
        
        if message.channel.id not in snipes:
            snipes[message.channel.id] = deque(maxlen=max_snipes)
        data = {"action": "deleted",
                "content": message.content,
                "sender": message.author.mention,
                "deleter": deleter,
                "time": self.bot.ftime.now()}
        snipes[message.channel.id].appendleft(data)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content: return
        if not before.guild: return
        if after.author.id == self.bot.user.id: return
        
        if before.channel.id not in snipes:
            snipes[before.channel.id] = deque(maxlen=max_snipes)
        data = {"action": "edited",
                "content": before.content + " --> " + after.content,
                "sender": before.author.mention,
                "message": before.jump_url,
                "time": self.bot.ftime.now()}
        snipes[before.channel.id].appendleft(data)

def setup(bot):
    bot.add_cog(snipe(bot))
