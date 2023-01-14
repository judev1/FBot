from discord.ext import commands
import asyncio

ongoing_purges = set()

class Purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["thanos", "zahando"])
    async def purge(self, ctx, *args):

        if not ctx.message.author.guild_permissions.manage_messages:
            await ctx.reply("You do not have the `manage_messages` permissions")
            return

        if ctx.channel.id in ongoing_purges:
            msg = await ctx.reply("A purge is already in progress")
            await asyncio.sleep(1)
            try: await msg.delete()
            except: pass
            return

        if len(args) != 0:
            limit = "".join(args)
            if limit.isdigit():
                limit = int(limit)
                if limit > 1000:
                    await ctx.reply("You cannot purge more than 1000 messages at a time")
                    return
                ongoing_purges.add(ctx.channel.id)
                await ctx.channel.purge(limit=limit + 1)
                ongoing_purges.remove(ctx.channel.id)
                msg = await ctx.send(f"Purged `{limit}` messages")
                await asyncio.sleep(1)
                await msg.delete()
                return

        await ctx.reply("You must specify how many messages to purge!")

async def setup(bot):
    await bot.add_cog(Purge(bot))