import discord, time
from Functions import Book
from discord.ext import commands
from Database import Database as db
from Functions import Functions as fn
from Triggers import trigger_response as tr

ver, fboturl, variables = fn.Get_Vars()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="treload")
    @commands.is_owner()
    async def _Treload(self, ctx):
        name = ctx.message.author.display_name
        start = time.time()
        tr.trigger_load()
        print(" > [dev] treload command by " + name)
        await ctx.send(f"`[dev] Reloaded triggers.csv in {str(round(time.time() - start, 4)*1000)}ms`")

    @commands.command(name="eval")
    @commands.is_owner()
    async def _Eval(self, ctx, *, content):
        try:
            evalcontent = eval(content)
            await ctx.send(f"FBot Eval: `{evalcontent}`")
            
        except Exception as e:
            if content == "":
                content = "NULL"
            await ctx.send(f"Failed to execute FBot Eval: `{content}`\nError: `{str(e)}`")

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

    @commands.command(name='load')
    @commands.is_owner()
    async def _LoadCog(self, ctx, cog):
        try:
            self.bot.load_extension("FBot_Cogs." + cog)
            await ctx.send(f"Loaded cog: `{cog}`")
        except Exception as e:
            await ctx.send(f"Failed to load cog: `{cog}`\nError: `{str(e)}`")

    @commands.command(name="unload")
    @commands.is_owner()
    async def _UnloadCog(self, ctx, cog):
        try:
            self.bot.unload_extension("FBot_Cogs." + cog)
            await ctx.send(f"Unloaded cog: `{cog}`")
        except Exception as e:
            await ctx.send(f"Failed to unload cog: `{cog}`\nError: `{str(e)}`")

    @commands.command(name="reload")
    @commands.is_owner()
    async def _ReloadCog(self, ctx, cog):
        try:
            self.bot.unload_extension("FBot_Cogs." + cog)
            self.bot.load_extension("FBot_Cogs." + cog)
            await ctx.send(f"Reloaded cog: `{cog}`")
        except Exception as e:
            await ctx.send(f"Failed to reload cog: `{cog}`\nError: `{str(e)}`")

    @commands.command(name="presence")
    @commands.is_owner()
    async def _ChangePresence(self, ctx, *, content):
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=content))

    @commands.command(name="send")
    @commands.is_owner()
    async def _Send(self, ctx, channel_id: int, *, message):
        channel = self.bot.get_channel(channel_id)
        
        if channel == None:
            await ctx.send("No channel found")
        else:
            await channel.send(message)

    @commands.command(name="newinvite")
    @commands.is_owner()
    async def _CreateInvite(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        
        try:
            invite = await guild.system_channel.create_invite(max_age=120 * 60, temporary=True)
        except:
            invite = "error resolving invite"
            
        await ctx.send(f"Created a temporary invite for `{guild}`\n"
                       f"`{invite}`, will expire after 2 hours")

    @commands.command(name="lookup")
    @commands.is_owner()
    async def _Lookup(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        
        if guild == None:
            await ctx.send("No guild found")
        else:
            memcount = 0
            botcount = 0
            
            for member in guild.members:
                if member.bot:
                    botcount += 1
                else:
                    memcount += 1
            
            await ctx.send(f"Guild found: `{guild}`\n`{memcount}` members and `{botcount}` bots")

    @commands.command(name="search")
    @commands.is_owner()
    async def _Search(self, ctx, *, query):

        query = query.lower()
        guild_list = []
        for guild in self.bot.guilds:
            if query in guild.name.lower():
                to_append = (guild.name, guild.id)
                guild_list.append(to_append)

        empty = "No matches found for `{query}`"
        pages, results = Book.Create_Pages(guild_list, "`%0` (`%1`)", empty=empty, getlines=True)
        await Book.Create_Book(self.bot, ctx, "FBot Search", pages, results=results)

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
        pages = Book.Create_Pages(guild_list, line, check_one=(2, 264445053596991498, False))
        await Book.Create_Book(self.bot, ctx, "FBot Servers", pages, header=header)
        

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
