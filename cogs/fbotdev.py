from traceback import format_exception
from discord.ext import commands
from datetime import datetime
from dbfn import reactionbook
import triggers as tr
import commands as cm
import discord
import socket
import modes
import time

def load(csv):
    start = time.time()
    csv.load()
    return round((time.time() - start) * 1000, 2) 

class fbotdev(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="csvreload")
    @commands.is_owner()
    async def _CSVReload(self, ctx):
        
        tms, cms = load(tr.tr), load(cm.cmds)
        embed = self.bot.fn.embed(ctx.author, "FBot csvreload",
                f"`[dev] Reloaded Triggers.csv in {tms}ms`",
                f"`[dev] Reloaded Commands.csv in {cms}ms`")
        await ctx.send(embed=embed)

    @commands.command(name="eval")
    @commands.is_owner()
    async def _Eval(self, ctx, *, content):

        bot = self.bot
        fn = bot.fn
        db = bot.db
        ftime = bot.ftime
        cache = bot.cache

        channel = ctx.channel
        author = ctx.author
        message = ctx.message

        if str(channel.type) != "private":
            guild = ctx.guild

        colour = self.bot.db.getcolour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Eval")
        
        try:
            result = str(eval(content))
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = []
        content = f"Input:\n```py\n{content}```\n"
        for i in range(0, len(result), 2000):
            pages.append(f"Output:\n```py\n{result[i : i + 2000]}\n```")
        if len(content + pages[0]) > 2000:
            pages.insert(0, content)
        else:
            pages[0] = content + pages[0]
        book.createpages(pages, ITEM_PER_PAGE=True)

        await book.createbook(MODE="arrows", COLOUR=colour, TIMEOUT=180)

    @commands.command(name="await")
    @commands.is_owner()
    async def _Await(SELF, CTX, FUNCTION, *, ARGS):
        global self, ctx, function, args
        self, ctx, function, args = SELF, CTX, FUNCTION, ARGS
        embed = self.bot.fn.embed(ctx.author, "FBot await",
                f"```python\nawait {function}({args})```")
        await ctx.send(embed=embed)
        exec(f"global temp\nasync def temp():\n    await {function}({args})")
        result = await temp()
        if result:
            embed = self.bot.fn.embed(ctx.author, "FBot results",
                f"```{result}```")
            await ctx.send(embed=embed)

    @commands.command(name="devon")
    @commands.is_owner()
    async def _FBotDevOn(self, ctx):
        self.bot.db.addchannel(ctx.channel.id, ctx.guild.id)
        self.bot.db.changestatus(ctx.channel.id, "on")
        await ctx.message.add_reaction("✅")

    @commands.command(name="devoff")
    @commands.is_owner()
    async def _FBotDevOff(self, ctx):
        self.bot.db.addchannel(ctx.channel.id, ctx.guild.id)
        self.bot.db.changestatus(ctx.channel.id, "off")
        await ctx.message.add_reaction("✅")

    @commands.command(name="devrespond")
    @commands.is_owner()
    @commands.guild_only()
    async def _Dev_Priority(self, ctx, *, arg):
        if arg in {"few", "some", "all"}:
            self.bot.db.changepriority(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("`Must be 'few', 'some', or 'all'`")

    @commands.command(name="devmodtoggle")
    @commands.is_owner()
    async def _Modtoggle(self, ctx, arg):
        self.bot.db.addchannel(ctx.channel.id, ctx.guild.id)
        if arg == "on":
            self.bot.db.changemodtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        elif arg == "off":
            self.bot.db.changemodtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")

    @commands.command(name="presence")
    @commands.is_owner()
    async def _ChangePresence(self, ctx, *, content):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name=content))
        await ctx.message.add_reaction("✅")

    @commands.command(name="send")
    @commands.is_owner()
    async def _Send(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(message)
        await ctx.message.add_reaction("✅")

    @commands.command(name="userdm")
    @commands.is_owner()
    async def _UserDM(self, ctx, user: discord.User, *, message):
        dm = await user.create_dm()
        await dm.send(message)
        await ctx.message.add_reaction("✅")

    @commands.command(name="newinvite")
    @commands.is_owner()
    async def _CreateInvite(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        try:
            invite = await guild.system_channel.create_invite(
                max_age=120 * 60, temporary=True)
        except: invite = "error resolving invite"
        await ctx.send(f"Created a temporary invite for `{guild}`\n"
                       f"`{invite}`, will expire after 2 hours")

    @commands.command(name="lookup")
    @commands.is_owner()
    async def _Lookup(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        if guild == None:
            embed = self.bot.fn.embed(ctx.author, "Lookup", "No guild found")
            await ctx.send(embed=embed)
        else:
            memcount = guild.member_count
            #memcount, botcount = 0, 0
            #for member in guild.members:
            #    if not member.bot:memcount += 1
            #    else: botcount += 1

            created = guild.created_at
            d = created.strftime("%d")
            mo = created.strftime("%m")
            y = created.strftime("%y")
            created = f"{d}/{mo}/{y}"

            embed = self.bot.fn.embed(guild.name, guild.description)
            embed.add_field(name="Members", value=memcount)# + botcount)
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

    @commands.command(name="cmdlist")
    @commands.is_owner()
    async def _CommandList(self, ctx):
        commands = [i.name for i in self.bot.walk_commands()]
        embed = self.bot.fn.embed(ctx.author, "FBot Commands",
                                  f" ```python\n{commands}```")
        await ctx.send(embed=embed)

    @commands.command(name="search")
    @commands.is_owner()
    async def _Search(self, ctx, *, query):
        query = query.lower()
        guild_list = []
        for guild in self.bot.guilds:
            if query in guild.name.lower():
                to_append = (guild.name, guild.id)
                guild_list.append(to_append)
        empty = f"No matches found for `{query}`"
        colour = self.bot.db.getcolour(ctx.author.id)
        book = reactionbook(self.bot, ctx)
        book.createpages(guild_list, "`%0` (`%1`)", EMPTY=empty)
        await book.createbook(TITLE="FBot Search", RESULTS=True, COLOUR=colour)

    #@commands.command(name="servers", aliases=["members"])
    #@commands.is_owner()
    #async def _Servers(self, ctx):
    #    guild_list = []
    #    for guild in self.bot.guilds:
    #        to_append = [len(guild.members), guild.name, guild.id]
    #        guild_list.append(to_append)
    #    guild_list = sorted(guild_list, reverse=True)
    #    line = f"Name: `%1`\nMembers `%0`"
    #    header = (f"Servers: `{len(self.bot.guilds) - 1}`\n"
    #              f"Members: `{sum(len(guild.members) for guild in self.bot.guilds) - len(self.bot.get_guild(264445053596991498).members)}`")
    #    pages = book.createpages(guild_list, line, check_one=(2, 264445053596991498, False))
    #    await book.createbook(self.bot, ctx, "FBot Servers", pages, header=header)

    @commands.command(name="host")
    @commands.is_owner()
    async def _Host(self, ctx):
        await ctx.send("This instance is running on: " + socket.gethostname())

def setup(bot):
    bot.add_cog(fbotdev(bot))