from discord.ext import tasks, commands
from triggers import tr
from datetime import datetime
from math import ceil


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

    def cog_unload(self):
        self.auto_stats.cancel()

    def get_stats_embed(self):
        fn = self.bot.fn
        hours = ceil((datetime.now().timestamp()-self.time_start)/3600)
        total = self.commands_processed + self.triggers_processed + self.other_messages_processed
        stats = f"""Commands processed: `{self.commands_processed}`
Triggers responded: `{self.triggers_processed}`
Messages ignored: `{self.other_messages_processed}`
Total count: `{total}`"""
        title = f"FBot stats for the past {hours} hours:"
        embed = fn.embed(title, stats)
        return embed
    

    @tasks.loop(hours = 24.0)
    async def auto_stats(self):
        if self.is_first_message:
            self.is_first_message = False
            return
        embed = self.get_stats_embed()
        await self.stats_channel.send(embed=embed)
        self.commands_processed = 0
        self.triggers_processed = 0
        self.other_messages_processed = 0
        self.time_start = datetime.now().timestamp()

    @commands.command(name="stats", aliases=["dailystats"])
    async def manual_stats(self, ctx):        
        embed = self.get_stats_embed()
        await ctx.send(embed=embed)
        
        

def setup(bot):
    bot.add_cog(dailystats(bot))





