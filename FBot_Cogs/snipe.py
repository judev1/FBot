from discord.ext import commands

snipes = dict()

class snipe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild: snipes[message.channel.id] = message

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild: snipes[before.channel.id] = before
    

    @commands.command(name="snipe")
    async def do_snipe(self, ctx):
        try:
            member = snipes[ctx.channel.id].author
            embed = self.bot.fn.embed("FBot Snipe",
                    f"```Sender: {member.display_name} ({member})\n"
                    f"Message: {snipes[ctx.channel.id].content}```")
            await ctx.send(embed=embed)
        except KeyError:
            embed = self.bot.fn.embed("FBot Snipe",
                    "```No recently deleted/edited messages to snipe```")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(snipe(bot))
