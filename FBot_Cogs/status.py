from discord.ext import commands
from functions import cooldown
from dbfn import reactionbook

class status(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="status")
    @commands.guild_only()
    @commands.check(cooldown)
    async def _Status(self, ctx):
        db = self.bot.db
        user = ctx.author

        if str(ctx.channel.type) == "private":
            embed = self.bot.fn.embed(user, "FBot is always on in DMs")
        else:
            db.Add_Channel(ctx.channel.id, ctx.guild.id)
            embed = self.bot.fn.embed(user, "FBot Status")
            embed.add_field(name="FBot Status", value=f"`{db.Get_Status(ctx.channel.id)}`")
            embed.add_field(name="Modtoggle", value=f"`{db.Get_Modtoggle(ctx.guild.id)}`")
            embed.add_field(name="Respond to", value=f"`{db.Get_Priority(ctx.guild.id)}`")
        await ctx.send(embed=embed)
        
    @commands.command(name="servstatus")
    @commands.guild_only()
    @commands.check(cooldown)
    async def _ServerStatus(self, ctx):
        db = self.bot.db
        user = ctx.author

        db.Add_Channel(ctx.channel.id, ctx.guild.id)
                
        guild_id = ctx.guild.id
        channels = db.Get_All_Status(guild_id)
        view_channel = "self.bot.get_channel(%0).overwrites_for(self.ctx.guild.default_role).pair()[1].view_channel"
        header = f"Modtoggle: `{db.Get_Modtoggle(guild_id)}` Responds to: `{db.Get_Priority(guild_id)}`"
        empty1 = "```There are no public channels\nin our database toggled on```"
        empty2 = "```There are no public channels\nin our database toggled off```"
        colour = self.bot.db.getcolour(user.id)

        book = reactionbook(self.bot, ctx, TITLE="FBot Server Status")
        book.createpages(channels, "<#%0>", EMPTY=empty1, SUBHEADER="**ON:**", check1=("%1", "on"), subcheck1=(view_channel, False))
        book.createpages(channels, "<#%0>", EMPTY=empty2, SUBHEADER="**OFF:**", check1=("%1", "off"), subcheck1=(view_channel, False))
        await book.createbook(HEADER=header, COLOUR=colour)
        
    @commands.command(name="servstatusmod")
    @commands.guild_only()
    @commands.check(cooldown)
    async def _ServerStatusMod(self, ctx):
        db = self.bot.db
        user = ctx.author
        
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")
            return
        
        guild = ctx.guild
        channels = db.Get_All_Status(guild.id)
        header = f"Modtoggle: `{db.Get_Modtoggle(guild.id)}` Responds to: `{db.Get_Priority(guild.id)}`"
        empty1 = "```There are no channels in\nour database toggled on```"
        empty2 = "```There are no channels in\nour database toggled off```"
        colour = self.bot.db.getcolour(user.id)

        book = reactionbook(self.bot, ctx, TITLE="FBot Server Status")
        book.createpages(channels, "<#%0>", EMPTY=empty1, SUBHEADER="**ON:**", check1=("%1", "on"))
        book.createpages(channels, "<#%0>", EMPTY=empty2, SUBHEADER="**OFF:**", check1=("%1", "off"))
        await book.createbook(HEADER=header, COLOUR=colour)

    @commands.command(name="on")
    async def _FBotOn(self, ctx):
        if not ctx.guild:
            await ctx.send("**FBot is always on in DMs.**")
            return
        db = self.bot.db
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "on")
            await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

    @commands.command(name="off")
    async def _FBotOff(self, ctx):
        if not ctx.guild:
            await ctx.send("**You can never turn off FBot in DMs.**")
            return
        db = self.bot.db
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "off")
            await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(status(bot))
