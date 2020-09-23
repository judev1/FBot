from discord.ext import commands
from functions import book
from functions import fn

class pns(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="patchnotes", aliases=["pn"])
    async def _PatchNotes(self, ctx, *arg):
        name = ctx.author.display_name
        send = ctx.send

        vers = sorted([i[0] for i in fn.getpatchnotevers()], reverse=True)

        try:
            arg = str(arg[0])
            if arg == "list":
                first = True
                for ver in vers:
                    if first:
                        formattedvers = ver
                        first = False
                    else: formattedvers += ", " + ver

                embed = fn.embed("**Patch Note Arguments**", f"`{formattedvers}`")
                embed = fn.footer(embed, name, "Patch notes")
                await send(embed=embed)
            elif arg + ".txt" in vers:
                pn, lines = fn.getpatchnotes(arg)
                pages = book.createpages([(arg, pn)], "```%1```", subheader="**Version %0**", lines=lines)
                await book.createbook(self.bot, ctx, "FBot Patch Notes", pages)
            else:
                embed = fn.errorembed("Invalid Argument",
                    f"The argument '{arg}' was not recognised, for all arguments use 'FBot pn list'")
                await send(embed=embed)
        except:
            first = True
            for ver in vers:
                pn, lines = fn.getpatchnotes(ver)
                if first:
                    pages = book.createpages([(ver, pn)], "```%1```", subheader="**Version %0**", lines=lines)
                    first = False
                else: pages = book.createpages([(ver, pn)], "```%1```", subheader="**Version %0**", lines=lines, pages=pages)
            await book.createbook(self.bot, ctx, "FBot Patch Notes", pages)

def setup(bot):
    bot.add_cog(pns(bot))
