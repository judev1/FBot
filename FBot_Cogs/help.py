from discord.ext import commands

class help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="help", aliases=["?"])
    async def _Help(self, ctx):
        fn = self.bot.fn
        
        embed = fn.embed("FBot Help",

                "**Useful Commands**\n"
                "Use `FBot on/off` to toggle fbot\n"
                "Use `FBot cmds` for a list of commands\n\n"

                "**Useful Links**\n"
                f"[Our Top.gg page]({fn.topgg}) and "
                f"[Join our server!]({fn.server})\n\n"

                "**You can help FBot too!**\n"
                f"[Vote here!]({fn.vote})")

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(help(bot))
