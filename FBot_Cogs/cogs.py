import discord
import os
from discord.ext import commands
from functions import book
from functions import fn

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
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[0][:-3]
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
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[0][:-3]
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
        if cog == "all":
            unable = []
            for cog in fn.getcogs():
                cog = cog[0][:-3]
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
        try:
            check = "'%0'[:-3] in [i for i in bot.cogs]"
            empty = "All cogs loaded"
            pages = book.createpages(fn.getcogs(), "%0", subheader="**Loaded:**", bot=self.bot, check_one=(check, True), lines=12)
            pages = book.createpages(fn.getcogs(), "%0", empty=empty, subheader="**Not loaded:**", bot=self.bot, check_one=(check, False), pages=pages, lines=12)
            await book.createbook(self.bot, ctx, "FBot Cogs", pages)
        except Exception as e:
            embed = fn.errorembed(f"failed to get cogs", str(e))
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cogs(bot))
