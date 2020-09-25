import discord
import functions
from database import db
from discord.ext import commands
from functions import book
from functions import fn

class status(commands.Cog):
    
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
                if str(ctx.channel.type) == "private": return
        
                try:
                    arg2 = arg[1]
                    if arg2 == "mod" and ctx.author.guild_permissions.administrator:
                        mod = True
                    elif arg2 == "mod":
                        await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")
                        return
                except: mod = False
                
                guild_id = ctx.guild.id
                channels = db.Get_All_Status(guild_id)
                one = "%1"
                view_channel = "bot.get_channel(%0).overwrites_for(ctx.guild.default_role).view_channel"
                header = f"Modtoggle: `{db.Get_Modtoggle(guild_id)}` Responds to: `{db.Get_Priority(guild_id)}`"
                empty1 = "`There are no channels`\n`in the Database set to on`"
                empty2 = "`There are no channels`\n`in the Database set to off`"

                if mod:
                    pages = book.createpages(channels, "<#%0>", empty=empty1, subheader="**ON:**", ctx=ctx, bot=self.bot, check_one=(one, "on"))
                    pages = book.createpages(channels, "<#%0>", empty=empty2, subheader="**OFF:**", ctx=ctx, bot=self.bot, check_one=(one, "off"), pages=pages)
                else:
                    pages = book.createpages(channels, "<#%0>", subheader="**ON:**", empty=empty1, ctx=ctx, bot=self.bot,
                                            check_one=(one, "on"), subcheck_one=(view_channel, True), subcheck_two=(view_channel, None))
                    pages = book.createpages(channels, "<#%0>", subheader="**OFF:**", empty=empty2, ctx=ctx, bot=self.bot, pages=pages,
                                            check_one=(one, "off"), subcheck_one=(view_channel, True), subcheck_two=(view_channel, None))
                await book.createbook(self.bot, ctx, "FBot Server Status", pages, header=header)
        except:
            if str(ctx.channel.type) == "private":
                embed = fn.embed("FBot is always on in DMs", "")
                embed.set_footer(text=f"Status requested by... you | Version v{fn.getinfo('ver')}", icon_url=functions.fboturl)
                await ctx.send(embed=embed)
            else:
                embed = fn.embed("FBot Status", "")
                embed.add_field(name="FBot Status", value=f"`{db.Get_Status(ctx.channel.id)}`")
                embed.add_field(name="Modtoggle", value=f"`{db.Get_Modtoggle(ctx.guild.id)}`")
                embed.add_field(name="Respond to", value=f"`{db.Get_Priority(ctx.guild.id)}`")
                embed = fn.footer(embed, name, "Status")
                await ctx.send(embed=embed)

    @commands.command(name="on")
    @commands.guild_only()
    async def _FBotOn(self, ctx):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        name = ctx.author.display_name
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "on")
            await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

    @commands.command(name="off")
    @commands.guild_only()
    async def _FBotOff(self, ctx):
        db.Add_Channel(ctx.channel.id, ctx.guild.id)
        name = ctx.author.display_name
        
        if ctx.author.guild_permissions.administrator or db.Get_Modtoggle(ctx.guild.id) == "off":
            db.Change_Status(ctx.channel.id, "off")
            await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(status(bot))
