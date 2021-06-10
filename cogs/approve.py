from discord.ext import commands

class approve(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="approve")
    async def _Approve(self, ctx, *args):

        content = "I'm FBot and I approve of this message"

        if args:
            await ctx.reply(content, mention_author=False)
        else:
            try: await ctx.message.delete()
            except: pass

            reference = ctx.message.reference
            if reference:
                msg = await ctx.fetch_message(id=reference.message_id)
                await msg.reply(content, mention_author=False)
            else:
                await ctx.send(content)

def setup(bot):
    bot.add_cog(approve(bot))