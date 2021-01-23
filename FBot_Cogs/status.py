from discord.ext import commands
from dbfn import reactionbook

class status(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="status")
    async def _Status(self, ctx, *args):
        db = self.bot.db
        if str(ctx.channel.type) != "private":
            db.Add_Channel(ctx.channel.id, ctx.guild.id)
        if len(args) == 2:
            if args[0] == "server":
                if str(ctx.channel.type) == "private": return
                try:
                    if args[1].lower() == "mod" and ctx.author.guild_permissions.administrator:
                        mod = True
                    elif args[1].lower() == "mod":
                        await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")
                        return
                except: mod = False
                
                guild_id = ctx.guild.id
                channels = db.Get_All_Status(guild_id)
                view_channel = "bot.get_channel(%l).overwrites_for(ctx.guild.default_role).view_channel"
                header = f"Modtoggle: `{db.Get_Modtoggle(guild_id)}` Responds to: `{db.Get_Priority(guild_id)}`"
                empty1 = "`There are no channels`\n`in the Database set to on`"
                empty2 = "`There are no channels`\n`in the Database set to off`"

                book = reactionbook(self.bot, ctx, TITLE="FBot Server Status")
                if mod:
                    book.createpages(channels, "<#%0>", EMPTY=empty1, SUBHEADER="**ON:**", check1=("%1", "on"))
                    book.createpages(channels, "<#%0>", EMPTY=empty2, SUBHEADER="**OFF:**", check1=("%1", "off"))
                else:
                    book.createpages(channels, "<#%0>", EMPTY=empty1, SUBHEADER="**ON:**", check1=("%1", "on"), subcheck1=(view_channel, None))
                    book.createpages(channels, "<#%0>", EMPTY=empty2, SUBHEADER="**OFF:**", check1=("%1", "off"), subcheck1=(view_channel, None))
                await book.createbook(HEADER=header, COLOUR=self.bot.fn.red)
        else:
            if str(ctx.channel.type) == "private":
                embed = self.bot.fn.embed("FBot is always on in DMs", "")
            else:
                embed = self.bot.fn.embed("FBot Status", "")
                embed.add_field(name="FBot Status", value=f"`{db.Get_Status(ctx.channel.id)}`")
                embed.add_field(name="Modtoggle", value=f"`{db.Get_Modtoggle(ctx.guild.id)}`")
                embed.add_field(name="Respond to", value=f"`{db.Get_Priority(ctx.guild.id)}`")
            await ctx.send(embed=embed)

    @commands.command(name="on")
    @commands.guild_only()
    async def _FBotOn(self, ctx):
        db = self.bot.db
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "on")
            await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

    @commands.command(name="off")
    @commands.guild_only()
    async def _FBotOff(self, ctx):
        db = self.bot.db
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "off")
            await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(status(bot))
