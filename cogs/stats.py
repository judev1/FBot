from discord.ext import commands
from functions import predicate
from triggers import tr
import commands as cm
from math import ceil
from time import time

class fakeuser: id = 0
fakeuser = fakeuser()

multi_ban = ("You're account has been flagged for high levels of spam, as such you have been banned from earning anymore multiplier. "
             "If this does not concern you, please carry on spamming! "
             "Otherwise if you think this is a mistake and would like to appeal your ban, "
             "please visit our support server: https://fbot.breadhub.uk/server")

class stats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.time_start = time()
        self.commands_processed = 0
        self.commands_ignored = 0
        self.triggers_processed = 0
        self.other_messages_processed = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        cache = self.bot.cache["RateLimits"]

        if user.bot: return
        if not commands.bot_has_permissions(send_messages=True):
            self.other_messages_processed += 1
            return
        if str(message.channel.type) == "private": guild_id = -1
        else: guild_id = message.guild.id

        multi = 1
        if self.bot.ftime.isweekend(): multi = 2
        fn, db = self.bot.fn, self.bot.db

        if db.isBanned(user.id):
            return

        fn, db = self.bot.fn, self.bot.db
        prefix = fn.getprefix(self.bot, message)
        commandcheck = message.content[len(prefix):]
        for command in cm.commands:
            if commandcheck.startswith(command):
                if db.Get_Cooldown(user.id) > 0:
                    self.commands_ignored += 1
                else:
                    if cache.check(user.id):
                        self.commands_processed += 1
                        db.usecommand(user.id)
                        if not db.isMultiBanned(user.id):
                            db.increasemultiplier(user.id, guild_id, multi * 2)
                    else:
                        db.multiBan(user.id, "true")
                        await message.channel.send(multi_ban)
                return

        for command in cm.devcmds:
            if commandcheck.startswith(command):
                if user.id in self.bot.owner_ids:
                    self.commands_processed += 1
                else:
                    self.commands_ignored += 1
                return

        if db.isTriggerBanned(user.id):
            return
        priority, status = "all", "on"
        if str(message.channel.type) != "private":
            db.Add_Channel(message.channel.id, guild_id)
            priority = db.Get_Priority(guild_id)
            status = db.Get_Status(message.channel.id)
        if status == "on":
            trigger_detected = tr.respond(message, priority)[0]
            if trigger_detected:
                if cache.check(user.id):
                    self.triggers_processed += 1
                    db.usetrigger(user.id)
                    if not db.isMultiBanned(user.id):
                        db.increasemultiplier(user.id, guild_id, multi)
                else:
                    db.multiBan(user.id, "true")
                    await message.channel.send(multi_ban)
                return
        self.other_messages_processed += 1

    def embed(self, user):
        fn = self.bot.fn
        hours = ceil((time() - self.time_start) / 3600)
        total = (self.commands_processed + self.commands_ignored +
                 self.triggers_processed + self.other_messages_processed)
        return fn.embed(user, f"FBot stats for the past {hours} hours:",
               f"Commands processed: `{self.commands_processed}`",
               f"Commands ignored: `{self.commands_ignored}`",
               f"Triggers responded: `{self.triggers_processed}`",
               f"Messages ignored: `{self.other_messages_processed}`",
               f"Total count: `{total}`")

    @commands.command(name="stats")
    @commands.check(predicate)
    async def _Stats(self, ctx):
        await ctx.send(embed=self.embed(ctx.author))

def setup(bot):
    bot.add_cog(stats(bot))