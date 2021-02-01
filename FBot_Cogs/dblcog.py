from discord.ext import commands, tasks
import dbl as DBL

class dblcog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.fn = bot.fn
        voteschannel = self.bot.get_channel(757722305395949572).send
        self.dblpy = DBL.DBLClient(self.bot, self.fn.gettoken(4),
            webhook_path="/dblwebhook", webhook_auth=self.fn.gettoken(5),
            webhook_port=6000)

    @commands.command(name="dbl")
    @commands.is_owner()
    async def _DBL(self, ctx):
        try:
            await self.dblpy.post_guild_count()
            embed = self.bot.fn.embed("DBL",
                    f"Updated server count: `{self.dblpy.guild_count()}`")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.bot.fn.errorembed("Failed To Update Server Count",
                    f"{type(e).__name__}: {e}")
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print("Test")
        print(data)
        embed = self.bot.fn.embed("FBot DBL vote", f"```{data}```")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("VOTE RECIEVED")
        print(data)
        embed = self.bot.fn.embed("FBot DBL vote", f"```{data}```")
        await self.voteschannel(embed=embed)

def setup(bot):
    bot.add_cog(dblcog(bot))
