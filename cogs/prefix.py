from discord.ext import commands

class prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    async def _ChangePrefix(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            fn, db = self.bot.fn, self.bot.db
            if arg == "reset":
                db.changeprefix(ctx.guild.id, "fbot")
                await ctx.message.add_reaction("✅")
            else:
                name = ctx.author.display_name
                if len(arg) > 10:
                    embed = fn.errorembed("Prefix too long",
                            f"Prefixes cannot be longer than 10 characters")
                    await ctx.send(embed=embed)
                    return

                char = fn.checkchars(arg)
                if char:
                    embed = fn.errorembed("Invalid Character",
                            f"The character ' {char} ' is not allowed")
                    await ctx.send(embed=embed)
                else:
                    db.changeprefix(ctx.guild.id, arg)
                    await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(prefix(bot))