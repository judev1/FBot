from discord.ext import commands
import discord

class DMs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        self.bot.dms = dict()
        self.bot.userdms = dict()

    @commands.command()
    async def dms(self, ctx):
        channel = await ctx.author.create_dm()
        await channel.send("What do you want from me?!?")
        emoji = self.bot.get_emoji(ctx.author.id)
        await ctx.message.add_reaction(emoji)

    @commands.command()
    async def send(self, ctx, channel: discord.TextChannel, *, content):
        await channel.send(content)
        await ctx.message.add_reaction("✅")

    @commands.command(name="opendm")
    async def _OpenDMs(self, ctx, user: discord.User, *, content):
        if ctx.channel.id in self.bot.dms:
            await ctx.reply("DM already open in this channel")
        else:
            for user in self.bot.userdms:
                if ctx.author.id == user:
                    await ctx.reply("DM already open with this user")
            try:
                channel = await user.create_dm()
                author = f"`{ctx.author}` "
                await channel.send(author + content)

                self.bot.dms[ctx.channel.id] = user
                self.bot.userdms[user.id] = ctx.channel

                await ctx.message.add_reaction("✅")
            except:
                await ctx.message.add_reaction("❌")

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.bot.ready():
            return

        if message.channel.id in self.bot.dms:
            if message.author.id in self.bot.owner_ids:
                user = self.bot.dms[message.channel.id]
                author = f"`{message.author}` "
                await user.dm_channel.send(author + message.content)
        elif message.author.id in self.bot.userdms:
            channel = self.bot.userdms[message.author.id]
            author = f"`{message.author}` "
            await channel.send(author + message.content)

    @commands.command(name="closedm")
    async def _CloseDMs(self, ctx):
        if ctx.channel.id not in self.bot.dms:
            await ctx.reply("No DM open in this channel")
        else:
            user = self.bot.dms[ctx.channel.id]
            del self.bot.dms[ctx.channel.id]
            del self.bot.userdms[user.id]

            await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(DMs(bot))