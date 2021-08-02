from discord.ext import commands
from dbfn import reactionbook
import lib.functions as fn
from discord import Embed

def format_unable(unable):
    first = True
    formatedunable = ""
    for cog in unable:
        if first:
            formatedunable = f" except:\n`{cog}`"
            first = False
        else: formatedunable += f", `{cog}`"
    return formatedunable

def errorembed(error, info):
    return Embed(title=f"**Error:** `{error}`",
            description=f"```{info}```", colour=fn.red)

class Cogs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def load(self, ctx, cog):
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                try: self.bot.load_extension("cogs." + cog)
                except Exception as e: unable.append(cog)
            embed = self.bot.embed(ctx.author, "FBot cogs",
                             "Loaded all cogs" + format_unable(unable))
        else:
            try:
                self.bot.load_extension("cogs." + cog)
                embed = self.bot.embed(ctx.author, "FBot cogs",
                                 f"Loaded cog: `{cog}`")
            except Exception as e:
                embed = errorembed(f"Failed to load cog: {cog}", str(e))
        await ctx.send(embed=embed)

    @commands.command()
    async def unload(self, ctx, cog):
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                if cog != "cogs":
                    try: self.bot.unload_extension("cogs." + cog)
                    except: unable.append(cog)
            embed = self.bot.embed(ctx.author, "FBot cogs",
                             "Unloaded all cogs" + format_unable(unable))
        else:
            try:
                self.bot.unload_extension("cogs." + cog)
                embed = self.bot.embed(ctx.author, "FBot cogs",
                                 f"Unloaded cog: `{cog}`")
            except Exception as e:
                embed = errorembed(f"Failed to unload cog: {cog}", str(e))
        await ctx.send(embed=embed)

    @commands.command()
    async def reload(self, ctx, cog):
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                try:
                    self.bot.unload_extension("cogs." + cog)
                    self.bot.load_extension("cogs." + cog)
                except: unable.append(cog)
            embed = self.bot.embed(ctx.author, "FBot cogs",
                             "Reloaded all cogs" + format_unable(unable))
        else:
            try:
                self.bot.unload_extension("cogs." + cog)
                self.bot.load_extension("cogs." + cog)
                embed = self.bot.embed(ctx.author, "FBot cogs",
                                 f"Reloaded cog: `{cog}`")
            except Exception as e:
                embed = errorembed(f"Failed to reload cog: {cog}", str(e))
        await ctx.send(embed=embed)

    @commands.command()
    async def cogs(self, ctx):
        colour = self.bot.get_colour(ctx.author.id)
        check = "'%l'[:-3] in self.bot.cogs"
        empty = "All cogs loaded"
        book = reactionbook(self.bot, ctx, TITLE="FBot Cogs")
        book.createpages(fn.getcogs(), EMPTY=empty,
                         SUBHEADER="**Loaded:**", check1=(check, True))
        book.createpages(fn.getcogs(), EMPTY=empty,
                         SUBHEADER="**Not Loaded:**", check1=(check, False))
        await book.createbook(MODE="numbers", COLOUR=colour)

def setup(bot):
    bot.add_cog(Cogs(bot))