from discord import AuditLogAction
from discord.ext import commands
from collections import deque
import lib.functions as fn
import discord
import os
import io

snipes = dict()
max_snipes = 10
message_delete = AuditLogAction.message_delete

class Snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def snipe(self, ctx, number=10):
        user = ctx.author
        if ctx.message.channel.id not in snipes:
            embed = self.bot.embed(user, "FBot Snipe",
                    "```No recently deleted/edited messages to snipe```")
            await ctx.reply(embed=embed)
            return

        if number < 1 or number > 10:
            await ctx.reply("`Number of snipes must be between 1 and 10`")
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
                if deleter == sender:
                    msg += f"\n{sender} deleted their own message at `{time}`"
                else:
                    msg += f"\n{deleter} deleted {sender}'s message at `{time}`"

            content = snipe["content"]
            if content == "":
                content = "`message's contents are unreadable`"
            msg += "\n" + content + "\n"

            i += 1
            if i == number: break

        if len(msg) > 1900:
            with io.open("fbot_snipe.txt", "w+", encoding="utf8") as file:
                file.write(msg)
            await ctx.reply(
                "`Sniped messages were longer than 2000 chars, sending as file:`",
                file=discord.File(r"fbot_snipe.txt"))
            os.remove("fbot_snipe.txt")
        else:
            embed = self.bot.embed(user, "FBot snipe", msg)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        if not self.bot.ready():
            return

        if not message.guild: return
        if message.author.bot: return

        bot_perms = message.channel.permissions_for(message.guild.get_member(self.bot.user.id))

        prefix = fn.getprefix(self.bot, message)
        commandcheck = message.content[len(prefix):]
        say_commands = tuple([command.name + " " for command in self.bot.commands if command.cog.qualified_name == "say"])
        if commandcheck.startswith(say_commands):
            if not message.author.bot:
                if  bot_perms.send_messages:
                    return

        deleter = "User"
        if bot_perms.view_audit_log:
            async for deleted in message.guild.audit_logs(limit=1, oldest_first=False, action=message_delete):
                if deleted.target.id == message.author.id:
                    deleter = deleted.user.mention
                else: deleter = message.author.mention

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

        if not self.bot.ready():
            return

        if before.content == after.content: return
        if not before.guild: return
        if after.author.bot: return

        if before.channel.id not in snipes:
            snipes[before.channel.id] = deque(maxlen=max_snipes)
        data = {"action": "edited",
                "content": before.content + " --> " + after.content,
                "sender": before.author.mention,
                "message": before.jump_url,
                "time": self.bot.ftime.now()}
        snipes[before.channel.id].appendleft(data)

async def setup(bot):
    await bot.add_cog(Snipe(bot))