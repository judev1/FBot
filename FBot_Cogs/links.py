import discord
from discord.ext import commands
from functions import *

class links(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="vote")
    async def _Vote(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed("FBot Vote", f"[Vote for FBot on Top.gg!]({voteurl})")
        embed = fn.footer(embed, name, "Vote")
        await ctx.send(embed=embed)

    @commands.command(name="invite")
    async def _Invite(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed("FBot Invite", f"[Invite FBot to your server!]({inviteurl})")
        embed = fn.footer(embed, name, "Invite")
        await ctx.send(embed=embed)

    @commands.command(name="Github", aliases=["github"])
    async def _Github(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed("FBot Github", f"[View FBots code on Github!]({githuburl})")
        embed = fn.footer(embed, name, "Github")
        await ctx.send(embed=embed)

    @commands.command(name="Topgg", aliases=["Top.gg", "topgg", "top.gg"])
    async def _TopGG(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed("FBot Top.gg", f"[View FBots Top.gg page!]({topggurl})")
        mbed = fn.footer(embed, name, "Tog.gg")
        await ctx.send(embed=embed)    

    @commands.command(name="server")
    async def _Server(self, ctx):
        name = ctx.message.author.display_name
        embed = fn.embed("FBot Server", f"[Join FBots server!]({serverurl})")
        embed = fn.footer(embed, name, "Server")
        await ctx.send(embed=embed)

    @commands.command(name="Minecraft", aliases=["minecraft", "mc"])
    async def _Minecraft(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed("Minecraft server down", "Currently our minecraft server is down,\n"
            "if you would like to see it come back contact a dev")
        #embed = discord.Embed(title="Join PURPLE HAZE x RIAS HUB x FBOT's Minecraft Server!",
        #                      description="We are a whitelist server so dm `@LinesGuy#9260` with your username to gain access\n\n"
        #                                  f"Also join [Purple Haze]({prplhzurl}), [Rias Hub]({rhurl}) and [FBot's Server]({serverurl})", colour=0xF42F42)
        embed = fn.footer(embed, name, "Minecraft")
        await ctx.send(embed=embed)

    @commands.command(name="links")
    async def _Links(self, ctx):
        name = ctx.author.display_name
        embed = fn.embed(
"FBot Links",
f"[Vote for FBot on Top.gg!]({voteurl})\n"
f"[Invite FBot to your server!]({inviteurl})\n"
f"[View FBots code on Github!]({githuburl})\n"
f"[View FBots Top.gg page!]({topggurl})\n"
f"[Join FBots server!]({serverurl})"
)
        embed = fn.footer(embed, name, "Links")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(links(bot))
