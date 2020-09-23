from discord.ext import commands
from functions import fn

class errorhandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"): return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound): pass

        elif isinstance(error, commands.DisabledCommand):
            embed = fn.errorembed("Command Not Found",
                             f"{ctx.command} has been disabled")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.NotOwner):
            embed = fn.errorembed("Missing Permissions",
                             f"you do not own this bot")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BadArgument):
            embed = fn.errorembed("Invalid Argument",
                             f"the argument you used was not recognised")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = fn.errorembed("Missing Argument",
                                  f"this command requires an argument")
            await ctx.send(embed=embed)
        else:
            send = self.bot.get_channel(743392645228920882).send
            embed = fn.embed(f"Error On Message `{ctx.message.content}`",
                             f"```Ignoring exception in command: {ctx.command}\n"
                             f"{error}```")
            await send(embed=embed)

def setup(bot):
    bot.add_cog(errorhandler(bot))