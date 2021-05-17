from discord.ext import commands
from discord import Embed
import commands as cm
import datetime
import time

class notices(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot: return

        prefix = self.bot.fn.getprefix(self.bot, message)
        commandcheck = message.content[len(prefix):]
        command_used = False
        for command in cm.commands:
            if commandcheck.startswith(command):
                command_used = True
                break
        
        if not command_used:
            return

        if str(message.channel.type) != "private":
            notice = self.bot.db.getlastnotice()
            last_notice = self.bot.db.getservernotice(message.guild.id)
            if last_notice < notice[0]:
                embed = self.notice(message, *notice)
                await message.channel.send(embed=embed)
                self.bot.db.updateservernotice(message.guild.id)
    
    def notice(self, ctx, date, title, message):
        
        fn, db = self.bot.fn, self.bot.db
        prefix = db.getprefix(ctx.guild.id)
        message = eval(f'f"""{message}"""')
        
        date = datetime.datetime.fromtimestamp(date)
        embed = self.bot.fn.embed(ctx.author, title, message)
        embed.set_author(name=date.strftime("%H:%M, %d/%m/%y UTC"))
        
        return embed

    @commands.command(name="getnotice")
    @commands.is_owner()
    async def _GetNotice(self, ctx):
        embed = self.notice(ctx, *self.bot.db.getlastnotice())
        await ctx.send(embed=embed)

    @commands.command(name="editnotice")
    @commands.is_owner()
    async def _EditNotice(self, ctx, *, text):
        title, message = text.split(" && ")
        self.bot.db.editnotice(title, message)
        await ctx.message.add_reaction("✅")

    @commands.command(name="notice")
    @commands.is_owner()
    async def _Notice(self, ctx, *, text):
        title, message = text.split(" && ")
        date = time.time()
        self.bot.db.addnotice(date, title, message)
        await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(notices(bot))