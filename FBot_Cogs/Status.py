import discord
from Functions import Book
from discord.ext import commands
from Database import Database as db
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="status")
    async def _Status(self, ctx, *arg):
        if str(ctx.channel.type) != "private":
            db.Add_Channel(ctx.channel.id, ctx.guild.id)
        name = ctx.author.display_name

        try:
            arg1 = arg[0]
            if arg1 == "server":
                if str(ctx.channel.type) == "private":
                    return
        
                try:
                    arg2 = arg[1]
                    if arg2 == "mod" and ctx.author.guild_permissions.administrator:
                        mod = True
                    elif arg2 == "mod":
                        await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")
                        return
                except:
                    mod = False
                
                guild_id = ctx.guild.id
                channels = db.Get_All_Status(guild_id)
                view_channel = "bot.get_channel(%0).overwrites_for(ctx.guild.default_role).view_channel"
                header = f"Modtoggle: `{db.Get_Modtoggle(guild_id)}` Responds to: `{db.Get_Priority(guild_id)}`"
                empty1 = "`There are no channels`\n`in the Database set to on`"
                empty2 = "`There are no channels`\n`in the Database set to off`"

                if mod:
                    pages = Book.Create_Pages(channels, "<#%0>", empty=empty1, subheader="**ON:**", ctx=ctx, bot=self.bot, check_one=(1, "on"))
                    pages = Book.Create_Pages(channels, "<#%0>", empty=empty2, subheader="**OFF:**", ctx=ctx, bot=self.bot, check_one=(1, "off"), pages=pages)
                else:
                    pages = Book.Create_Pages(channels, "<#%0>", subheader="**ON:**", empty=empty1, ctx=ctx, bot=self.bot,
                                            check_one=(1, "on"), subcheck_one=(view_channel, True), subcheck_two=(view_channel, None))
                    pages = Book.Create_Pages(channels, "<#%0>", subheader="**OFF:**", empty=empty2, ctx=ctx, bot=self.bot, pages=pages,
                                            check_one=(1, "off"), subcheck_one=(view_channel, True), subcheck_two=(view_channel, None))
                    
                await Book.Create_Book(self.bot, ctx, "FBot Server Status", pages, header=header)
        
        except:
            if str(ctx.channel.type) == "private":
                embed = discord.Embed(title="FBot is always on in DMs", colour=0xF42F42)
                embed.set_footer(text=f"Status requested by... you | Version v{ver}", icon_url=fboturl)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="FBot Status", colour=0xF42F42)
                embed.add_field(name="FBot Status", value=f"`{db.Get_Status(ctx.channel.id)}`")
                embed.add_field(name="Modtoggle", value=f"`{db.Get_Modtoggle(ctx.guild.id)}`")
                embed.add_field(name="Respond to", value=f"`{db.Get_Priority(ctx.guild.id)}`")
                embed.set_footer(text=f"Status requested by {name} | Version v{ver}", icon_url=fboturl)
                await ctx.send(embed=embed)

    @commands.command(name="on")
    @commands.guild_only()
    async def _FBotOn(self, ctx):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        name = ctx.author.display_name
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "on")
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

    @commands.command(name="off")
    @commands.guild_only()
    async def _FBotOff(self, ctx):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        name = ctx.author.display_name
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "off")
            await ctx.message.add_reaction("✅")
        else:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
