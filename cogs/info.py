from discord.ext import commands
from functions import predicate
from triggers import tr
import commands as cm
from math import ceil
from time import time


class fakeuser:
    id = 0


fakeuser = fakeuser()

multi_ban = ("You're account has been flagged for high levels of spam, as such you have been banned from earning anymore multiplier. "
             "If this does not concern you, please carry on spamming! "
             "Otherwise if you think this is a mistake and would like to appeal your ban, "
             "please visit our support server: https://fbot.breadhub.uk/server")


class info(commands.Cog):

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

        if user.bot:
            return
        if not commands.bot_has_permissions(send_messages=True):
            self.other_messages_processed += 1
            return
        if str(message.channel.type) == "private":
            guild_id = -1
        else:
            guild_id = message.guild.id

        multi = 1
        if self.bot.ftime.isweekend():
            multi = 2
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

    @commands.command(name="info")
    @commands.check(predicate)
    async def _Info(self, ctx):

        ftime = self.bot.ftime
        fn = self.bot.fn

        totalmembers = 0
        for servers in self.bot.guilds:
            totalmembers += servers.member_count

        embed = self.bot.fn.embed(ctx.author, "FBot Info")
        embed.add_field(name="Session start", value=ftime.start)
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Last Updated", value=fn.getinfo("lastupdated"))
        embed.add_field(name="Uptime", value=ftime.uptime())
        embed.add_field(name="Members", value=totalmembers)
        embed.add_field(name="Version", value=fn.getinfo("ver"))
        await ctx.send(embed=embed)

    @commands.command(name="servinfo")
    @commands.check(predicate)
    async def _ServInfo(self, ctx):
        guild = ctx.guild

        memcount = guild.member_count
        #memcount, botcount = 0, 0
        # for member in guild.members:
        #    if not member.bot:memcount += 1
        #    else: botcount += 1

        created = guild.created_at
        d = created.strftime("%d")
        mo = created.strftime("%m")
        y = created.strftime("%y")
        created = f"{d}/{mo}/{y}"

        embed = self.bot.fn.embed(ctx.author, guild.name)  # guild.description
        embed.add_field(name="Members", value=memcount)  # + botcount)
        #embed.add_field(name="Users", value=memcount)
        #embed.add_field(name="Bots", value=botcount)
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        #embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Language", value=guild.preferred_locale)
        embed.add_field(name="Created", value=created)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="session", aliases=["uptime"])
    @commands.check(predicate)
    async def _Session(self, ctx):
        ftime = self.bot.ftime
        embed = self.bot.fn.embed(ctx.author, "FBot's Session")
        embed.add_field(name="Session start", value=ftime.start)
        embed.add_field(name="Uptime", value=ftime.uptime())
        await ctx.send(embed=embed)

    @commands.command(name="ver")
    @commands.check(predicate)
    async def _Version(self, ctx):
        fn = self.bot.fn
        ver, updated = fn.getinfo("ver"), fn.getinfo("lastupdated")
        embed = fn.embed(ctx.author, "FBot's Version")
        embed.add_field(name="Version", value=f"`{ver}`")
        embed.add_field(name="Released", value=f"`{updated}`")
        await ctx.send(embed=embed)

    @commands.command(name="premium")
    @commands.check(predicate)
    async def _Premium(self, ctx):
        await ctx.send("https://fbot.breadhub.uk/premium")


def setup(bot):
    bot.add_cog(info(bot))
