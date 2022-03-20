from traceback import format_exception
from discord.ext import commands
from dbfn import reactionbook
import discord

import lib.functions as fn

class Errorhandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_bot_ready(self):
        errorlogs = self.bot.settings.channels.errors
        self.errorlogs = self.bot.get_channel(errorlogs)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, "on_error"): return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        error_type = type(error)

        if error_type is commands.CommandNotFound:
            return
        elif error_type is commands.MissingPermissions:
            return
        elif error_type is commands.NotOwner:
            return
        elif error_type is commands.MessageNotFound:
            return
        elif error_type is commands.DisabledCommand:
            await ctx.reply("**This command is disabled.** If you'd like to find out more join our support server")
        elif error_type is commands.BadArgument:
            await ctx.reply("**Bad argument.** Whoops! Looks like one of the arguments you entered is a bit off...")
        elif error_type is commands.MissingRequiredArgument:
            await ctx.reply("**Command missing an argument.** Whoops! You've missed an argument for this command")
        elif error_type is commands.NoPrivateMessage:
            await ctx.reply("**Server only command.** This command can only be used in a server")
        elif error_type is commands.UserNotFound:
            await ctx.reply("**No user found.** Hmm we couldn't find that user, maybe try something else")
        elif error_type is commands.CommandOnCooldown:
            retry = round(error.retry_after, 2)
            await ctx.reply(f"**You're on cooldown!.** Please wait `{retry}s` to use this command", delete_after=5)
        elif error_type is commands.CheckFailure:
            error = str(error)
            errorlines = error.split("\n")
            embed = self.bot.embed(fn.user, errorlines[0], *errorlines[2:])
            try:
                try: await ctx.send(embed=embed)
                except: await ctx.reply(error)
            except:
                try:
                    channel = await ctx.author.create_dm()
                    await channel.send(embed=embed)
                except: pass
        elif error_type is commands.UserNotFound:
            await ctx.reply("User not found")
        elif error_type is commands.ChannelNotFound:
            await ctx.reply("Channel not found")
        elif error_type is commands.GuildNotFound:
            await ctx.reply("Guild not found")
        else:
            if error_type is commands.CommandInvokeError:
                if type(error.original) is discord.Forbidden:
                    error = error.original
                    if error.text == "Missing Permissions":
                        try:
                            await ctx.reply("FBot is missing permissions to complete this action")
                        except:
                            channel = await ctx.author.create_dm()
                            await channel.send(f"FBot doesn't have permissions to send messages in <#{ctx.message.id}>")
                        return
                elif type(error.original) is discord.errors.NotFound:
                    if error.original.text == "Unknown User":
                        await ctx.reply("Looks like that member doesn't exist")
                        return
                    await ctx.reply(error.original.text)

            embed = self.bot.embed(
                ctx.author, "An unusual error has occurred",
                "The devs have been notified, please contact:\n"
                "`@justjude#2296` or `@Lines#9260`\nOR join our "
                f"[support server]({fn.links.server}) and give us a ping"
            )

            try:
                await ctx.send(embed=embed)
            except:
                try:
                    channel = await ctx.author.create_dm()
                    await channel.send(embed=embed)
                except: pass

            ctx.channel = self.errorlogs
            book = reactionbook(self.bot, ctx, TITLE="Error Log")
            result = "".join(format_exception(error, error, error.__traceback__))

            pages = list()
            content = f"Error on message:\n```{ctx.message.content}```"
            content += f"```by {ctx.message.author.name} ({ctx.message.author.id})```"
            content += f"```{ctx.message.channel.type} channel (server: {ctx.message.guild})```"
            for i in range(0, len(result), 2000):
                pages.append(f"```py\n{result[i:i + 1000]}\n```")
            if len(content + pages[0]) > 2000:
                pages.insert(0, content)
            else:
                pages[0] = content + pages[0]
            book.createpages(pages, ITEM_PER_PAGE=True)

            await book.createbook(MODE="arrows", COLOUR=fn.colours.red, TIMEOUT=180)

def setup(bot):
    bot.add_cog(Errorhandler(bot))