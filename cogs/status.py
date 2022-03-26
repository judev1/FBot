from discord.ext import commands
from dbfn import reactionbook

import lib.database as db

circle = {"off": ":red_circle:", "on": ":green_circle:"}
volume = {"few": ":mute:", "some": ":sound:", "all": ":loud_sound:"}
on = circle["on"] + " **ON:**"
off = circle["off"] + " **OFF:**"
emptyon = "```There are no channels in\nour database toggled on```"
emptyoff = emptyon.replace("on", "off")

class Status(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def config(self, ctx):
        user = ctx.author

        if str(ctx.channel.type) == "private":
            embed = self.bot.embed(user, "FBot is always on in DMs")
        else:
            db.addchannel(ctx.channel.id, ctx.guild.id)

            status = db.getstatus(ctx.channel.id)
            modtoggle = db.getmodtoggle(ctx.guild.id)
            priority = db.getpriority(ctx.guild.id)
            mode = db.getmode(ctx.guild.id)
            language = db.getlang(ctx.guild.id)

            embed = self.bot.embed(user, "FBot Config",
                    f"{circle[status]} FBot is `{status}`",
                    f"{circle[modtoggle]} Modtoggle is `{modtoggle}`",
                    f"{volume[priority]} Responds to `{priority}`")
            embed.add_field(name="Speak", value=f"`{mode}`")
            embed.add_field(name="Language", value=f"`{language}`")

        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx):
        user = ctx.author
        db.addchannel(ctx.channel.id, ctx.guild.id)

        guild_id = ctx.guild.id
        channels = db.getallstatus(guild_id)
        view_channel = "self.bot.get_channel(%0).overwrites_for(self.ctx.guild.default_role).pair()[1].view_channel"

        modtoggle = db.getmodtoggle(ctx.guild.id)
        priority = db.getpriority(ctx.guild.id)
        header = f"{circle[modtoggle]} Modtoggle is `{modtoggle}`\n{volume[priority]} Responds to `{priority}`"
        colour = self.bot.get_colour(user.id)

        book = reactionbook(self.bot, ctx, TITLE="FBot Status")
        book.createpages(channels, "<#%0>", EMPTY=emptyon, SUBHEADER=on, check1=("%1", "on"), subcheck1=(view_channel, False))
        book.createpages(channels, "<#%0>", EMPTY=emptyoff, SUBHEADER=off, check1=("%1", "off"), subcheck1=(view_channel, False))
        await book.createbook(HEADER=header, COLOUR=colour)

    @commands.command()
    async def modstatus(self, ctx):
        user = ctx.author
        db.addchannel(ctx.channel.id, ctx.guild.id)

        if not ctx.author.guild_permissions.administrator:
            await ctx.reply("Only members with administrator privileges can toggle this")
            return

        guild = ctx.guild
        channels = db.getallstatus(guild.id)

        modtoggle = db.getmodtoggle(ctx.guild.id)
        priority = db.getpriority(ctx.guild.id)
        header = f"{circle[modtoggle]} Modtoggle is `{modtoggle}`\n{volume[priority]} Responds to `{priority}`"
        colour = self.bot.get_colour(user.id)

        book = reactionbook(self.bot, ctx, TITLE="FBot Mod Status")
        book.createpages(channels, "<#%0>", EMPTY=emptyon, SUBHEADER=on, check1=("%1", "on"))
        book.createpages(channels, "<#%0>", EMPTY=emptyoff, SUBHEADER=off, check1=("%1", "off"))
        await book.createbook(HEADER=header, COLOUR=colour)

    @commands.command()
    async def on(self, ctx):
        if not ctx.guild:
            await ctx.reply("**FBot is always on in DMs**")
            return
        db.addchannel(ctx.channel.id, ctx.guild.id)

        if ctx.author.guild_permissions.administrator or db.getmodtoggle(ctx.guild.id) == "off":
            db.setstatus(ctx.channel.id, "on")
            emoji = self.bot.get_emoji(ctx.author.id)
            await ctx.message.add_reaction(emoji)
        else: await ctx.reply("Only members with administrator privileges can toggle this")

    @commands.command()
    async def off(self, ctx):
        if not ctx.guild:
            await ctx.reply("**You can never turn off FBot in DMs**")
            return
        db.addchannel(ctx.channel.id, ctx.guild.id)

        if ctx.author.guild_permissions.administrator or db.getmodtoggle(ctx.guild.id) == "off":
            db.setstatus(ctx.channel.id, "off")
            emoji = self.bot.get_emoji(ctx.author.id)
            await ctx.message.add_reaction(emoji)
        else: await ctx.reply("Only members with administrator privileges can toggle this")

def setup(bot):
    bot.add_cog(Status(bot))