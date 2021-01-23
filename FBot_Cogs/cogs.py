from discord.ext import commands
from dbfn import reactionbook

def formatunable(unable):
    first = True
    formatedunable = ""
    for cog in unable:
        if first:
            formatedunable = f" except:\n`{cog}`"
            first = False
        else: formatedunable += f", `{cog}`"
    return formatedunable


class cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
    @commands.is_owner()
    async def _LoadCog(self, ctx, cog):
        fn = self.bot.fn
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                try: self.bot.load_extension("FBot_Cogs." + cog)
                except Exception as e: unable.append(cog)
            embed = fn.embed("FBot cogs", "Loaded all cogs" + formatunable(unable))
        else:
            try:
                self.bot.load_extension("FBot_Cogs." + cog)
                embed = fn.embed("FBot cogs", f"Loaded cog: `{cog}`")
            except Exception as e:
                embed = fn.errorembed(f"failed to load cog: {cog}", str(e))
        await ctx.send(embed=embed)

    @commands.command(name="unload")
    @commands.is_owner()
    async def _UnloadCog(self, ctx, cog):
        fn = self.bot.fn
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                if cog != "cogs":
                    try: self.bot.unload_extension("FBot_Cogs." + cog)
                    except: unable.append(cog)
            embed = fn.embed("FBot cogs", "Unloaded all cogs" + formatunable(unable))
        else:
            try:
                self.bot.unload_extension("FBot_Cogs." + cog)
                embed = fn.embed("FBot cogs", f"Unloaded cog: `{cog}`")
            except Exception as e:
                embed = fn.errorembed(f"failed to unload cog: {cog}", str(e))
        await ctx.send(embed=embed)

    @commands.command(name="reload")
    @commands.is_owner()
    async def _ReloadCog(self, ctx, cog):
        fn = self.bot.fn
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[:-3]
                try:
                    self.bot.unload_extension("FBot_Cogs." + cog)
                    self.bot.load_extension("FBot_Cogs." + cog)
                except: unable.append(cog)
            embed = fn.embed("FBot cogs", "Reloaded all cogs" + formatunable(unable))
        else: 
            try:
                self.bot.unload_extension("FBot_Cogs." + cog)
                self.bot.load_extension("FBot_Cogs." + cog)
                embed = fn.embed("FBot cogs", f"Reloaded cog: `{cog}`")
            except Exception as e:
                embed = fn.errorembed(f"failed to reload cog: {cog}", str(e))
        await ctx.send(embed=embed)

    @commands.command(name="cogs")
    @commands.is_owner()
    async def _Cogs(self, ctx):
        fn = self.bot.fn
        #try:
        if True:
            check = "'%l'[:-3] in self.bot.cogs"
            empty = "All cogs loaded"
            book = reactionbook(self.bot, ctx, TITLE="FBot Cogs")
            book.createpages(self.bot.fn.getcogs(), EMPTY=empty,
                             SUBHEADER="**Loaded:**", check1=(check, True))
            book.createpages(self.bot.fn.getcogs(), EMPTY=empty,
                             SUBHEADER="**Not Loaded:**", check1=(check, False))
            await book.createbook(MODE="numbers", COLOUR=fn.red)
        #except Exception as e:
        #    embed = fn.errorembed(f"failed to get cogs", str(e))
        #    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cogs(bot))
