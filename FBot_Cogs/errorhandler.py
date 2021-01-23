from discord.ext import commands

class errorhandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.errorlogs = bot.get_channel(743392645228920882)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"): return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error = getattr(error, "original", error)
        fn = self.bot.fn

        if isinstance(error, commands.CommandNotFound): return

        elif isinstance(error, commands.DisabledCommand):
            embed = fn.errorembed("Command Not Found",
                    f"{ctx.command} has been disabled")
        elif isinstance(error, commands.MissingPermissions):
            embed = fn.errorembed("Missing Permissions",
                    "The bot is missing permissions to execute the command")
        elif isinstance(error, commands.NotOwner):
            embed = fn.errorembed("Missing Permissions",
                    f"You do not own this bot")
        elif isinstance(error, commands.BadArgument):
            embed = fn.errorembed("Invalid Argument",
                    f"The argument you used was not recognised")
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = fn.errorembed("Missing Argument",
                    f"This command is missing an argument")
        else:
            try:
                embed = fn.embed("An unusual error has occurred",
                        "The devs have been notified, please contact:\n"
                        "`@justjude#2296` or `@LinesGuy#9260`\n"
                        f"OR join our [support server]({fn.server}) "
                        "and give us a ping")
                try:
                    await ctx.channel.send(embed=embed)
                except:
                    channel = await ctx.author.create_dm()
                    await channel.send(embed=embed)
                    
                embed = fn.embed(f"Error On Message `{ctx.message.content}`",
                        f"```Ignoring exception in command: {ctx.command}```"
                        f"```{error}``````{ctx.message}```")
                await self.errorlogs.send(embed=embed)
            except: pass
            finally: return
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(errorhandler(bot))
