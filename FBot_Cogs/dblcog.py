from discord.ext import commands, tasks
import dbl as DBL

class dblcog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        fn = bot.fn
        self.dblpy = DBL.DBLClient(self.bot, fn.gettoken(4),
            webhook_path=fn.gettoken(5), webhook_auth=fn.gettoken(6),
            webhook_port=int(fn.gettoken(7)))

    @commands.command(name="dbl")
    @commands.is_owner()
    async def _DBL(self, ctx):
        try:
            await self.dblpy.post_guild_count()
            embed = fn.embed("DBL",
                    f"Updated server count: `{self.dblpy.guild_count()}`")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = fn.errorembed("Failed To Update Server Count",
                    f"{type(e).__name__}: {e}")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("VOTE RECIEVED")
        print(data)
        channel = self.bot.get_channel(757722305395949572)
        embed = self.bot.fn.embed("FBot DBL vote", f"```{data}```")
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(dblcog(bot))
