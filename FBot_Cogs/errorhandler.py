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

        fn = self.bot.fn
        if type(error) is commands.CommandNotFound:
            return
        elif type(error) is commands.DisabledCommand:
            embed = fn.errorembed("Command Not Found",
                    f"{ctx.command} has been disabled")
        elif type(error) is commands.MissingPermissions:
            embed = fn.errorembed("Missing Permissions",
                    "The bot is missing permissions to execute the command")
        elif type(error) is commands.NotOwner:
            embed = fn.errorembed("Missing Permissions",
                    f"Only FBot Devs can run this command")
        elif type(error) is commands.BadArgument:
            embed = fn.errorembed("Invalid Argument",
                    f"The argument you used was not recognised")
        elif type(error) is commands.MissingRequiredArgument:
            embed = fn.errorembed("Missing Argument",
                    f"This command is missing an argument")
        elif type(error) is commands.NoPrivateMessage:
            embed = fn.errorembed("Server-only command",
                    f"This command cannot be used outside of servers.")
        elif type(error) is commands.UserNotFound:
            embed = fn.errorembed("User not found",
                    f"Invalid user parameter. Check command help.")
        elif type(error) is commands.CommandOnCooldown:
            if error.retry_after < 10:
                retry = str(error.cooldown) + "` seconds"
            if error.retry_after < 120:
                retry = str(round(error.retry_after)) + "` seconds"
            else: retry = str(round(error.retry_after / 60)) + "` mins"
            embed = fn.embed("You are being ratelimited",
                    f"You may use this command again in `{retry}")
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
                    try:
                        channel = await ctx.author.create_dm()
                        await channel.send(embed=embed)
                    except: pass

                error = getattr(error, "original", error)
                embed = fn.embed(f"Error On Message `{ctx.message.content}`",
                        f"```Ignoring exception in command: {ctx.command}```"
                        f"```{error}``````{ctx.message}```")
                await self.errorlogs.send(embed=embed)
            except: pass
            finally: return
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(errorhandler(bot))
