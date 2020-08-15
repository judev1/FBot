import discord
from discord.ext import commands

class FBot_Cogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        """This prevents any commands with local handlers being
        handled here in on_command_error."""
        if hasattr(ctx.command, 'on_error'):
            return

        """This prevents any cogs with an overwritten
        cog_command_error being handled here."""
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, 'original', error)

        if isinstance(error, commands.CommandNotFound):
            pass

        elif isinstance(error, commands.DisabledCommand):
            embed = discord.Embed(title="**Error:** `Command not found`", description=f"```{ctx.command} has been disabled```", colour=0xF42F42)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.NotOwner):
            embed = discord.Embed(title="**Error:** `Missing permissions`", description=f"```You do not own this bot```", colour=0xF42F42)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title="**Error:** `Invalid Argument`", description=f"```The argument you used was not recognised```", colour=0xF42F42)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="**Error:** `Missing Argument`", description=f"```This command requires an argument```", colour=0xF42F42)
            await ctx.send(embed=embed)

        else:
            # All other Errors not returned come here
            send = self.bot.get_channel(743392645228920882).send
            embed = discord.Embed(title="**Error:**", description=f"Error on message: `{ctx.message.content}`\n"
                                                                  f"Ignoring exception in command: `{ctx.command}`\n"
                                                                  f"```{error}```", colour=0xF42F42)
            await send(embed=embed)


def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
