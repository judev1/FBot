from discord.ext import commands

class Approve(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def approve(self, ctx, *args):

        content = "Hello I'm FBot and I approve of this message"

        if args:
            await ctx.reply(content, mention_author=False)
        else:
            try: await ctx.message.delete()
            except: pass

            reference = ctx.message.reference
            if reference:
                message = await ctx.fetch_message(reference.message_id)
                await message.reply(content, mention_author=False)
            else:
                await ctx.send(content)

async def setup(bot):
    await bot.add_cog(Approve(bot))