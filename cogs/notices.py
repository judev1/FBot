from discord.ext import commands
import lib.functions as fn
import lib.commands as cm
import datetime
import time

class Notices(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.bot.ready():
            return


        if message.author.bot: return

        if str(message.channel.type) == "private":
            return

        bot_perms = message.channel.permissions_for(message.guild.get_member(self.bot.user.id))
        if not bot_perms.send_messages:
            return

        prefix = await fn.getprefix(self.bot, message)
        if not message.content.startswith(prefix):
            return
        commandcheck = message.content[len(prefix):]
        command_used = False
        for command in cm.commands:
            if commandcheck.startswith(command):
                command_used = True
                break

        if not command_used:
            return

        notice = await self.bot.db.getlastnotice()
        if notice:
            last_notice = await self.bot.db.getservernotice(message.guild.id)
            if last_notice < notice[0]:
                embed = self.create_notice(message, *notice)
                await message.channel.send(embed=embed)
                await self.bot.db.updateservernotice(message.guild.id)

    def create_notice(self, ctx, date, title, message):
        message = eval(f'f"""{message}"""')

        date = datetime.datetime.fromtimestamp(date)
        embed = self.bot.embed(ctx.author, title, message)
        embed.set_author(name=date.strftime("%H:%M, %d/%m/%y UTC"))

        return embed

    @commands.command()
    async def getnotice(self, ctx):
        embed = self.create_notice(ctx, *await self.bot.db.getlastnotice())
        await ctx.send(embed=embed)

    @commands.command()
    async def editnotice(self, ctx, *, text):
        title, message = text.split(" && ")
        await self.bot.db.editnotice(title, message)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def notice(self, ctx, *, text):
        title, message = text.split(" && ")
        date = time.time()
        await self.db.addnotice(date, title, message)
        await ctx.message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(Notices(bot))