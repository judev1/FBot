import discord
from discord.ext import commands
import asyncio

class PurgeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge", aliases=["zahando", "thanos", "clear"])
    async def do_purge(self, ctx, *, limit):
        
        if limit.isdigit():
            limit = int(limit)
        else:
            await ctx.send("You must specify how many messages to delete!")
            return
        
        if ctx.author.guild_permissions.manage_messages or ctx.author.id in self.bot.owner_ids:
            await ctx.channel.purge(limit=limit + 1)
            # + 1 to include the purge command
            msg = await ctx.send(f"`Deleted {limit} messages.`")
            await asyncio.sleep(1)
            await msg.delete()
        else:
            await ctx.send("You do not have the `manage_messages` permission!")

    @do_purge.error
    async def purge_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'limit':
                await ctx.send("You must specify how many messages to delete!")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

            await ctx.send("`An error occurred while executing this command.`")

            
    

def setup(bot):
    bot.add_cog(PurgeCog(bot))
