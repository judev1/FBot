from discord.ext import commands

class links(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="vote")
    async def _Vote(self, ctx):
        fn = self.bot.fn
        embed = fn.embed("FBot Vote", f"[Vote for FBot on Top.gg!]({fn.vote})")
        await ctx.send(embed=embed)

    @commands.command(name="invite")
    async def _Invite(self, ctx):
        fn = self.bot.fn
        embed = fn.embed("FBot Invite", f"[Invite FBot to your server!]({fn.invite})")
        await ctx.send(embed=embed)

    @commands.command(name="Github", aliases=["github"])
    async def _Github(self, ctx):
        fn = self.bot.fn
        embed = fn.embed("FBot Github", f"[View FBots code on Github!]({fn.github})")
        await ctx.send(embed=embed)

    @commands.command(name="Topgg", aliases=["Top.gg", "topgg", "top.gg"])
    async def _TopGG(self, ctx):
        fn = self.bot.fn
        embed = fn.embed("FBot Top.gg", f"[View FBots Top.gg page!]({fn.topgg})")
        await ctx.send(embed=embed)    

    @commands.command(name="server")
    async def _Server(self, ctx):
        fn = self.bot.fn
        embed = fn.embed("FBot Server", f"[Join FBots server!]({fn.server})")
        await ctx.send(embed=embed)

    @commands.command(name="Minecraft", aliases=["minecraft", "mc"])
    async def _Minecraft(self, ctx):
        fn = self.bot.fn
        #embed = fn.embed("Minecraft server down", "Currently our minecraft server is down,\n"
        #    "if you would like to see it come back contact a dev")
        embed = fn.embed(title="Join FBOT's Modded Minecraft Server!",
                info=f"Come to our server ({fn.server}) to find out more")
        await ctx.send(embed=embed)

    @commands.command(name="links")
    async def _Links(self, ctx):
        fn = self.bot.fn
        embed = fn.embed("FBot Links",
                f"[Vote for FBot on Top.gg!]({fn.vote})\n"
                f"[Invite FBot to your server!]({fn.invite})\n"
                f"[View FBots code on Github!]({fn.github})\n"
                f"[View FBots Top.gg page!]({fn.topgg})\n"
                f"[Join FBots server!]({fn.server})")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(links(bot))
