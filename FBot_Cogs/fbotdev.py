import discord
import math
import random
import time
import socket
from discord.ext import commands
from database import db
from functions import book
from functions import fn
from triggers import tr

class fbotdev(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="treload")
    @commands.is_owner()
    async def _Treload(self, ctx):
        name = ctx.message.author.display_name
        start = time.time()
        tr.trigger_load()
        ms = round(time.time() - start, 4) * 1000
        embed = fn.embed("FBot treload",
                         f"`[dev] Reloaded triggers.csv in {ms}ms`")
        await ctx.send(embed=embed)

    @commands.command(name="eval")
    @commands.is_owner()
    async def _Eval(self, ctx, *, content):
        try:
            evalcontent = eval(content)
            embed = fn.embed("FBot eval", f" ```{evalcontent}```")
            await ctx.send(embed=embed)
        except Exception as e:
            if content == "": content = "NULL"
            embed = fn.embed(f"Error in `{content}`", f"```{str(e)}```")
            await ctx.send(embed=embed)

    @commands.command(name="devon")
    @commands.is_owner()
    @commands.guild_only()
    async def _FBotStatus(self, ctx):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        db.Change_Status(ctx.channel.id, "on")
        await ctx.message.add_reaction("✅")

    @commands.command(name="devoff")
    @commands.is_owner()
    @commands.guild_only()
    async def _FBotStatus(self, ctx):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        db.Change_Status(ctx.channel.id, "off")
        await ctx.message.add_reaction("✅")

    @commands.command(name="devmodtoggle")
    @commands.is_owner()
    @commands.guild_only()
    async def _Modtoggle(self, ctx, arg):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        if arg == "on":
            db.Change_Modtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")
        elif arg == "off":
            db.Change_Modtoggle(ctx.guild.id, arg)
            await ctx.message.add_reaction("✅")

    @commands.command(name="presence")
    @commands.is_owner()
    async def _ChangePresence(self, ctx, *, content):
        await self.bot.change_presence(status=discord.Status.online,
                                       activity=discord.Game(name=content))
        await ctx.message.add_reaction("✅")

    @commands.command(name="send")
    @commands.is_owner()
    async def _Send(self, ctx, channel_id: int, *, message):
        channel = self.bot.get_channel(channel_id)
        if channel == None: 
            embed = fn.errorembed(f"failed to send", "channel not found")
            await ctx.send(embed=embed)
        else: await channel.send(message)
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
            embed = fn.embed("Lookup", "No guild found")
            await ctx.send(embed=embed)
        else: 
            memcount, botcount = 0, 0
            for member in guild.members:
                if not member.bot:memcount += 1
                else: botcount += 1

            created = guild.created_at
            d = created.strftime("%d")
            mo = created.strftime("%m")
            y = created.strftime("%y")
            created = f"{d}/{mo}/{y}"

            embed = fn.embed(guild.name, guild.description)
            embed.add_field(name="Members", value=memcount + botcount)
            embed.add_field(name="Users", value=memcount)
            embed.add_field(name="Bots", value=botcount)
            embed.add_field(name="Voice channels", value=len(guild.voice_channels))
            embed.add_field(name="Text channels", value=len(guild.text_channels))
            embed.add_field(name="Roles", value=len(guild.roles))
            embed.add_field(name="Owner", value=guild.owner)
            embed.add_field(name="Language", value=guild.preferred_locale)
            embed.add_field(name="Created", value=created)
            embed.set_thumbnail(url=guild.icon_url)
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
        pages, results = book.createpages(guild_list, "`%0` (`%1`)", empty=empty, getlines=True)
        await book.createbook(self.bot, ctx, "FBot Search", pages, results=results)

    @commands.command(name="servers", aliases=["members"])
    @commands.is_owner()
    async def _Servers(self, ctx):
        guild_list = []
        for guild in self.bot.guilds:
            to_append = [len(guild.members), guild.name, guild.id]
            guild_list.append(to_append)
        guild_list = sorted(guild_list, reverse=True)
        line = f"Name: `%1`\nMembers `%0`"
        header = (f"Servers: `{len(self.bot.guilds) - 1}`\n"
                  f"Members: `{sum(len(guild.members) for guild in self.bot.guilds) - len(self.bot.get_guild(264445053596991498).members)}`")
        pages = book.createpages(guild_list, line, check_one=(2, 264445053596991498, False))
        await book.createbook(self.bot, ctx, "FBot Servers", pages, header=header)

    @commands.command(name="host")
    @commands.is_owner()
    async def _Host(self, ctx):
        msg = f"This instance is running on: {socket.gethostname()}"
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(fbotdev(bot))