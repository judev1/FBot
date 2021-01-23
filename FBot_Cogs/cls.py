from discord.ext import commands
from dbfn import reactionbook

class cls(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="changelogs", aliases=["changelog", "cl", "cls"])
    async def _PatchNotes(self, ctx, *args):

        fn = self.bot.fn
        vers = fn.getvers()

        arg = " ".join(args)
        if arg != "":
            if arg == "list":
                fvers = "`, `".join(vers)
                embed = fn.embed("**Change Log Arguments**", f"`{fvers}`")
            elif arg in vers:
                embed = fn.embed("**FBot Change Logs**",
                        f"**Version {arg}**\n```{fn.getcls(arg)}```")
            else:
                embed = fn.errorembed("Invalid Version",
                    f"That version is invalid, for all versions use 'FBot cl list'")
            await ctx.send(embed=embed)
        else:
            data = []
            for ver in vers:
                data.append((ver, fn.getcls(ver)))
            book = reactionbook(self.bot, ctx, TITLE="FBot Change Logs")
            book.createpages(data, LINE="**Version %0**\n```%1```", ITEM_PER_PAGE=True)
            await book.createbook(COLOUR=fn.red)

def setup(bot):
    bot.add_cog(cls(bot))
