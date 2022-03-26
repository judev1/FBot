from discord.ext import commands
import datetime
import time

import lib.functions as fn
import lib.database as db

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


        if not fn.getcommand(self.bot, message, ignore_dev=False):
            return

        notice = db.getnotice()
        if notice:
            last_notice = db.getservernotice(message.guild.id)
            if last_notice < notice[0]:
                embed = self.create_notice(message, *notice)
                await message.channel.send(embed=embed)
                db.setservernotice(message.guild.id)

    def create_notice(self, ctx, date, title, message):
        message = eval(f'f"""{message}"""')

        date = datetime.datetime.fromtimestamp(date)
        embed = self.bot.embed(ctx.author, title, message)
        embed.set_author(name=date.strftime("%H:%M, %d/%m/%y UTC"))

        return embed

    @commands.command()
    async def getnotice(self, ctx):
        embed = self.create_notice(ctx, *db.getnotice())
        await ctx.send(embed=embed)

    @commands.command()
    async def editnotice(self, ctx, *, text):
        title, message = text.split(" && ")
        db.setnotice(title, message)
        await ctx.message.add_reaction("✅")

    @commands.command()
    async def notice(self, ctx, *, text):
        title, message = text.split(" && ")
        date = time.time()
        db.addnotice(date, title, message)
        await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(Notices(bot))