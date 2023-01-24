from discord.ext import commands
from lib.triggers import tr
import lib.functions as fn
import lib.commands as cm
from math import ceil
from time import time

class stats:

    def __init__(self):
        self.set()

    def set(self):
        self.commands_processed = 0
        self.commands_ratelimited = 0
        self.triggers_processed = 0
        self.other_messages_processed = 0

class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.time_start = time()
        bot.stats = stats()

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.bot.ready():
            return

        user = message.author
        stats = self.bot.stats

        if user.bot:
            return
        if not commands.bot_has_permissions(send_messages=True):
            stats.other_messages_processed += 1
            return
        if str(message.channel.type) == "private":
            guild_id = fn.guild.id
        else:
            guild_id = message.guild.id

        prefix = await fn.getprefix(self.bot, message)
        commandcheck = message.content[len(prefix):]
        for command in cm.commands:
            if commandcheck.startswith(command):
                return
        for command in cm.devcmds:
            if commandcheck.startswith(command):
                return

        priority, status = "all", "on"
        if str(message.channel.type) != "private":
            await self.bot.db.addchannel(message.channel.id, guild_id)
            priority = await self.bot.db.getpriority(guild_id)
            status = await self.bot.db.getstatus(message.channel.id)
        if status == "on":
            trigger_detected = tr.respond(message, priority)[0]
            if trigger_detected:
                stats.triggers_processed += 1
                await self.bot.db.usetrigger(user.id)
                return
        stats.other_messages_processed += 1

    def embed(self, user):
        stats = self.bot.stats
        hours = ceil((time() - self.time_start) / 3600)
        total = (stats.commands_processed + stats.commands_ratelimited +
                 stats.triggers_processed + stats.other_messages_processed)
        return self.bot.embed(user, f"FBot stats for the past {hours} hours:",
                          f"Commands processed: `{stats.commands_processed}`",
                          f"Commands ratelimited: `{stats.commands_ratelimited}`",
                          f"Triggers responded: `{stats.triggers_processed}`",
                          f"Messages ignored: `{stats.other_messages_processed}`",
                          f"Total count: `{total}`")

    @commands.command(name="stats")
    async def _Stats(self, ctx):
        await ctx.send(embed=self.embed(ctx.author))

    @commands.command(name="info")
    async def _Info(self, ctx):

        ftime = self.bot.ftime

        totalmembers = 0
        for servers in self.bot.guilds:
            totalmembers += servers.member_count

        embed = self.bot.embed(ctx.author, "FBot Info")
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Users", value=totalmembers)
        embed.add_field(name="Shards", value=self.bot.shard_count)
        embed.add_field(name="Session start", value=ftime.start)
        embed.add_field(name="Uptime", value=ftime.uptime())
        await ctx.send(embed=embed)

    @commands.command(name="servinfo")
    async def _ServerInfo(self, ctx):
        guild = ctx.guild

        memcount = guild.member_count

        created = guild.created_at
        d = created.strftime("%d")
        mo = created.strftime("%m")
        y = created.strftime("%y")
        created = f"{d}/{mo}/{y}"

        embed = self.bot.embed(ctx.author, guild.name)
        embed.add_field(name="Members", value=memcount)
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Language", value=guild.preferred_locale)
        embed.add_field(name="Created", value=created)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await ctx.send(embed=embed)

    @commands.command(name="perms", aliases=["permissions"])
    async def _Perms(self, ctx):

        bot_perms = ctx.channel.permissions_for(
            ctx.guild.get_member(self.bot.user.id)
        )

        functional = dict()
        optional = dict()
        for perm in cm.functional:
            bot_perm = getattr(bot_perms, perm)
            functional[perm] = bot_perm
        for perm in cm.optional:
            bot_perm = getattr(bot_perms, perm[1:-1])
            optional[perm[1:-1]] = bot_perm

        def formatperms(perms):
            pages = list()
            for perm in perms:
                pages.append(f"{fn.emojis[perms[perm]]} ~ {fn.formatperm(perm)}")
            return "\n".join(pages)

        embed = self.bot.embed(
            ctx.author,
            f"**FBot's Permissions in #{ctx.channel}**"
        )
        embed.add_field(
            name="Functional Permissions",
            value=formatperms(functional)
        )
        embed.add_field(
            name="Optional Permissions",
            value=formatperms(optional)
        )

        await ctx.send(embed=embed)

    @commands.command(name="premium")
    async def _Premium(self, ctx):
        await ctx.reply("https://fbot.breadhub.uk/premium")

    @commands.command()
    async def devs(self, ctx):
        embed = self.bot.embed(ctx.author, title="This is the team that makes FBot great!")
        embed.add_field(name="Developers", value="justjude#2296 (<@!671791003065384987>)\nLines#9260 (<@!216260005827969024>)\nCodeize#0001 (<@!668423998777982997>)\nScreaMyCZE#0016 (<@!311178459919417344>)\n\nIf you have any questions or concerns, or just\nwant to hang out, click the link in the next\n embed to join the support server!")
        await ctx.reply(embed=embed)
        await ctx.invoke(self.bot.get_command("server"))

    @commands.command()
    async def dev(self, ctx):
        await ctx.reply(f"Yeah {ctx.author.mention} is a dev, that's why he can use this command")

async def setup(bot):
    await bot.add_cog(Info(bot))
