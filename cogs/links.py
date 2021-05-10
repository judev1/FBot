from discord.ext import commands
from discord import Embed

class links(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def _Invite(self, ctx):
        fn = self.bot.fn
        embed = fn.embed(ctx.author, "Invite FBot to your server!", url=fn.invite)
        await ctx.send(embed=embed)

    @commands.command(name="server")
    async def _Server(self, ctx):
        fn = self.bot.fn
        embed = fn.embed(ctx.author, "Join our server, it's for support and fun!", url=fn.server)
        await ctx.send(embed=embed)

    @commands.command(name="links")
    async def _Links(self, ctx):
        
        fn = self.bot.fn
        embed = fn.embed(ctx.author, "FBot links",)
        
        embed.add_field(name="General",
        value=f"[Support server]({fn.server}) :small_blue_diamond: [Invite FBot]({fn.invite})")
        embed.add_field(name="External",
        value=f"[Our Website]({fn.site}) :small_blue_diamond: [FBot's Github]({fn.github})")

        
        embed.add_field(name="Botlists", inline=False,
        value=f"[top.gg]({fn.top}) :small_blue_diamond: [discordbotlist.com]({fn.dbl}) :small_blue_diamond: " +
        f"[botsfordiscord.com]({fn.bfd}) :small_blue_diamond: [discord.bots.gg]({fn.dbgg})\n" +
        f"[listcord.xyz]({fn.lixyz}) :small_blue_diamond: [discord-botlist.eu]({fn.dbeu}) :small_blue_diamond:" +
        f"[botlist.space]({fn.blsp}) :small_blue_diamond: [botlist.me]({fn.blme})")
       
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(links(bot))