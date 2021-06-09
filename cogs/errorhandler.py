from traceback import format_exception
from discord.ext import commands
from dbfn import reactionbook
import discord

class fakeuser: id = 0
user = fakeuser()

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
        elif type(error) is commands.MissingPermissions:
            return
        elif type(error) is commands.NotOwner:
            return
        elif type(error) is commands.MessageNotFound:
            return
        elif type(error) is commands.DisabledCommand:
            await ctx.send("**This command is disabled**\n" +
                  "If you'd like to find out more join our support server")
        elif type(error) is commands.BadArgument:
            await ctx.send("**Bad argument**\n" +
                  "Whoops! Looks like one of the arguments you entered is a bit off...")
        elif type(error) is commands.MissingRequiredArgument:
            await ctx.send("**Command missing an argument**\n" +
                  "Whoops! You've missed an argument for this command")
        elif type(error) is commands.NoPrivateMessage:
            await ctx.send("**Server only command**\n" +
                  "This command can only be used in a server")
        elif type(error) is commands.UserNotFound:
            await ctx.send("**No user found**\n" +
                  "Hmm we couldn't find that user, maybe try something else")
        elif type(error) is commands.CommandOnCooldown:
            retry = round(error.retry_after, 2)
            await ctx.send("**You're on cooldown!**\n" +
                  f"Please wait `{retry}s` to use this command")
        elif type(error) is commands.CheckFailure:
            error = str(error)
            errorlines = error.split("\n")
            embed = fn.embed(user, errorlines[0], *errorlines[2:])
            try:
                try:
                    await ctx.send(embed=embed)
                except: await ctx.send(error)
            except:
                try:
                    channel = await ctx.author.create_dm()
                    try:
                        await channel.send(embed=embed)
                    except: await channel.send(error)
                except: pass
        elif type(error) is commands.UserNotFound:
            await ctx.send("User not found")
        elif type(error) is commands.ChannelNotFound:
            await ctx.send("Channel not found")
        elif type(error) is commands.GuildNotFound:
            await ctx.send("Guild not found")
        else:
            if type(error) is commands.CommandInvokeError:
                if type(error.original) is discord.Forbidden:
                    error = error.original
                    if error.text == "Missing Permissions":
                        embed = fn.errorembed(error.text,
                        f"FBot doesn't have permissions to send a message in that channel")
                        channel = await ctx.author.create_dm()
                        await channel.send(embed=embed)
                        return
                elif type(error.original) is discord.errors.NotFound:
                    if error.original.text == "Unknown User":
                        await ctx.channel.send("Looks like that member doesn't exist")
                        return
                    #elif error.original.text == "Unknown Message":
                    #    await ctx.channel.send("Looks like that member doesn't exist")
                    #    return
                    await ctx.channel.send(error.original.text)
            embed = fn.embed(ctx.author, "An unusual error has occurred",
                    "The devs have been notified, please contact:\n"
                    "`@justjude#2296` or `@Lines#9260`\n"
                    f"OR join our [support server]({fn.server}) "
                    "and give us a ping")
            try:
                try:
                    await ctx.channel.send(embed=embed)
                except:
                    try:
                        channel = await ctx.author.create_dm()
                        await channel.send(embed=embed)
                    except: pass

                ctx.channel = self.errorlogs
                colour = self.bot.db.getcolour(ctx.author.id)
                book = reactionbook(self.bot, ctx, TITLE="Error Log")
                result = "".join(format_exception(error, error, error.__traceback__))

                pages = []
                content = f"Error on message:\n```{ctx.message.content}```"
                content += f"```by {ctx.message.author.name} ({ctx.message.author.id})```"
                content += f"```{ctx.message.channel.type} channel (server: {ctx.message.guild})```"
                for i in range(0, len(result), 2000):
                    pages.append(f"```py\n{result[i : i + 1000]}\n```")
                if len(content + pages[0]) > 2000:
                    pages.insert(0, content)
                else:
                    pages[0] = content + pages[0]
                book.createpages(pages, ITEM_PER_PAGE=True)

                await book.createbook(MODE="arrows", COLOUR=fn.red, TIMEOUT=180)
            except: pass

def setup(bot):
    bot.add_cog(errorhandler(bot))