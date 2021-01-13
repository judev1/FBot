from discord.ext import commands
import asyncio
import sys

class purge(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", aliases=["zahando", "thanos", "clear"])
    async def do_purge(self, ctx, *args):

        if len(args) != 0:
            limit = "".join(args)
            if limit.isdigit(): limit = int(limit)
            else:
                await ctx.send("You must specify how many messages to purge!")
                return
            
            if ctx.author.guild_permissions.manage_messages or ctx.author.id in self.bot.owner_ids:
                await ctx.channel.purge(limit=limit + 1)
                msg = await ctx.send(f"`Purged {limit} messages.`")
                await asyncio.sleep(1)
                await msg.delete()
            else: await ctx.send("You do not have the `manage_messages` permission!")
        else:
            await ctx.send("You must specify how many messages to purge!")
    
def setup(bot):
    bot.add_cog(purge(bot))
