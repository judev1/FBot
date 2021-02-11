from discord.ext import tasks, commands
from functions import cooldown
from datetime import datetime
from triggers import tr
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
        self.triggers_processed = 0
        self.other_messages_processed = 0
        self.auto_stats.start()
        self.is_first_message = True

    @commands.Cog.listener()
    async def on_message(self, message):
        fn, db = self.bot.fn, self.bot.db
        commandcheck = message.content[len(fn.getprefix(self.bot, message)):]
        user, guild = message.author, message.guild
        for command in self.bot.walk_commands():
            if commandcheck.startswith(command.name):
                self.commands_processed += 1
                return
            for alias in command.aliases:
                if commandcheck.startswith(alias):
                    self.commands_processed += 1
                    return
        priority, status = "all", "on"
        if str(message.channel.type) != "private":
            db.Add_Channel(message.channel.id, message.guild.id)
            priority = db.Get_Priority(message.guild.id)
            status = db.Get_Status(message.channel.id)
        if status == "on":
            trigger_detected = tr.trigger_respond(message, priority)[0]
            if trigger_detected:
                self.triggers_processed += 1
        else:
            self.other_messages_processed += 1

    @commands.command(name="stats")
    @commands.check(cooldown)
    async def manual_stats(self, ctx):
        await ctx.send(embed=self.get_stats_embed(ctx.author))

    def get_stats_embed(self, user):
        fn = self.bot.fn
        hours = ceil((datetime.now().timestamp()-self.time_start)/3600)
        total = self.commands_processed + self.triggers_processed + self.other_messages_processed
        stats = f"""Commands processed: `{self.commands_processed}`
Triggers responded: `{self.triggers_processed}`
Messages ignored: `{self.other_messages_processed}`
Total count: `{total}`"""
        return fn.embed(user, f"FBot stats for the past {hours} hours:", stats)

    def cog_unload(self):
        self.auto_stats.cancel()
    
    @tasks.loop(hours = 24.0)
    async def auto_stats(self):
        if self.is_first_message:
            self.is_first_message = False
            return
        embed = self.get_stats_embed(fakeuser)
        await self.stats_channel.send(embed=embed)
        self.commands_processed = 0
        self.triggers_processed = 0
        self.other_messages_processed = 0
        self.time_start = datetime.now().timestamp()
        
def setup(bot):
    bot.add_cog(dailystats(bot))
