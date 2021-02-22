from discord.ext import tasks, commands
from functions import cooldown
from datetime import datetime
from triggers import tr
import commands as cm
from math import ceil

class fakeuser: id = 0
fakeuser = fakeuser()

class dailystats(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.stats_channel = self.bot.get_channel(803050054095994900) # fbot 1
        #self.stats_channel = self.bot.get_channel(727320090483359844) # fbot 3
        self.time_start = datetime.now().timestamp()
        self.commands_processed = 0
        self.commands_ignored = 0
        self.triggers_processed = 0
        self.other_messages_processed = 0
        self.auto_stats.start()
        self.is_first_message = True

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author

        if user.bot: return
        if not commands.bot_has_permissions(send_messages=True):
            self.other_messages_processed += 1
            return
        if str(message.channel.type) == "private": guild_id = -1
        else: guild_id = message.guild.id

        bonus = 1
        if self.bot.ftime.isweekend(): bonus = 2
        fn, db = self.bot.fn, self.bot.db
        
        fn, db = self.bot.fn, self.bot.db
        prefix = fn.getprefix(self.bot, message)
        commandcheck = message.content[len(prefix):]
        for command in cm.commands:
            if commandcheck.startswith(command):
                if db.Get_Cooldown(user.id) > 0:
                    self.commands_ignored += 1
                else:
                    db.increasemultiplier(user.id, guild_id, 2 * bonus)
                    if db.premium(user.id):
                        db.Update_Cooldown(user.id, 2)
                    else: db.Update_Cooldown(user.id, 8)
                    self.commands_processed += 1
                return
        for command in cm.devcmds:
            if commandcheck.startswith(command):
                if user.id in self.bot.owner_ids:
                    self.commands_processed += 1
                else:
                    self.commands_ignored += 1
                return
        
        priority, status = "all", "on"
        if str(message.channel.type) != "private":
            db.Add_Channel(message.channel.id, guild_id)
            priority = db.Get_Priority(guild_id)
            status = db.Get_Status(message.channel.id)
        if status == "on":
            trigger_detected = tr.respond(message, priority)[0]
            if trigger_detected:
                db.increasemultiplier(user.id, guild_id, 1 * bonus)
                self.triggers_processed += 1
                return
        self.other_messages_processed += 1

    def embed(self, user):
        fn = self.bot.fn
        hours = ceil((datetime.now().timestamp()-self.time_start)/3600)
        total = (self.commands_processed + self.commands_ignored +
                 self.triggers_processed + self.other_messages_processed)
        stats = (f"Commands processed: `{self.commands_processed}`",
                 f"Commands ignored: `{self.commands_ignored}`",
                 f"Triggers responded: `{self.triggers_processed}`",
                 f"Messages ignored: `{self.other_messages_processed}`",
                 f"Total count: `{total}`")
        return fn.embed(user, f"FBot stats for the past {hours} hours:", *stats)

    def cog_unload(self):
        self.auto_stats.cancel()

    @commands.command(name="stats")
    @commands.check(cooldown)
    async def manual_stats(self, ctx):
        await ctx.send(embed=self.embed(ctx.author))
    
    @tasks.loop(hours = 24.0)
    async def auto_stats(self):
        if self.is_first_message:
            self.is_first_message = False
            return
        await self.stats_channel.send(embed=self.embed(fakeuser))
        self.commands_processed = 0
        self.commands_ignored = 0
        self.triggers_processed = 0
        self.other_messages_processed = 0
        self.time_start = datetime.now().timestamp()
        
def setup(bot):
    bot.add_cog(dailystats(bot))
