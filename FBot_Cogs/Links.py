import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars(var1="voteurl", var2="inviteurl", var3="githuburl", var4="topggurl", var5="serverurl", var6="prplhzurl", var7="rhurl")
voteurl = variables[0]
inviteurl = variables[1]
githuburl = variables[2]
topggurl = variables[3]
serverurl = variables[4]
prplhzurl = variables[5]
rhurl = variables[6]

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="vote")
    async def _Vote(self, ctx):
        name = ctx.author.display_name
        
        embed = discord.Embed(title="FBot Vote", description=f"[Vote for FBot on Top.gg!]({voteurl})", colour=0xF42F42)
        embed.set_footer(text=f"Vote requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="invite")
    async def _Invite(self, ctx):
        name = ctx.author.display_name

        embed = discord.Embed(title="FBot Invite", description=f"[Invite FBot to your server!]({inviteurl})", colour=0xF42F42)
        embed.set_footer(text=f"Invite requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="Github", aliases=["github"])
    async def _Github(self, ctx):
        name = ctx.author.display_name

        embed = discord.Embed(title="FBot Github", description=f"[View FBots code on Github!]({githuburl})", colour=0xF42F42)
        embed.set_footer(text=f"Github requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="Topgg", aliases=["Top.gg", "topgg", "top.gg"])
    async def _TopGG(self, ctx):
        name = ctx.author.display_name

        embed = discord.Embed(title="FBot Top.gg", description=f"[View FBots Top.gg page!]({topggurl})", colour=0xF42F42)
        embed.set_footer(text=f"Top.gg requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)    

    @commands.command(name="server")
    async def _Server(self, ctx):
        name = ctx.message.author.display_name

        embed = discord.Embed(title="FBot Server", description=f"[Join FBots server!]({serverurl})", colour=0xF42F42)
        embed.set_footer(text=f"Server requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="Minecraft", aliases=["minecraft", "mc"])
    async def _Minecraft(self, ctx):
        name = ctx.author.display_name

        embed = discord.Embed(title="Server down", colour=0xF42F42)
        #embed = discord.Embed(title="Join PURPLE HAZE x RIAS HUB x FBOT's Minecraft Server!",
        #                      description="We are a whitelist server so dm `@LinesGuy#9260` with your username to gain access\n\n"
        #                                  f"Also join [Purple Haze]({prplhzurl}), [Rias Hub]({rhurl}) and [FBot's Server]({serverurl})", colour=0xF42F42)
        embed.set_footer(text=f"Minecraft requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="links")
    async def _Links(self, ctx):
        name = ctx.author.display_name

        embed = discord.Embed(title="FBot Links", description=f"[Vote for FBot on Top.gg!]({voteurl})\n"
                                                              f"[Invite FBot to your server!]({inviteurl})\n"
                                                              f"[View FBots code on Github!]({githuburl})\n"
                                                              f"[View FBots Top.gg page!]({topggurl})\n"
                                                              f"[Join FBots server!]({serverurl})", colour=0xF42F42)
        embed.set_footer(text=f"Links requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
