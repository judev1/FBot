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
                if arg.startswith(("'", '"')) or arg.endswith(("'", '"')):
                    arg = arg[1:-1]
                if len(arg) > 10:
                    embed = fn.errorembed("Prefix too long",
                            f"Prefixes cannot be longer than 10 characters")
                    await ctx.send(embed=embed)
                else:
                    db.changeprefix(ctx.guild.id, arg)
                    await ctx.message.add_reaction("✅")
                    await ctx.reply(f"Use `{arg}help` or {self.bot.user.mention} if you get stuck")
            return

        await ctx.reply("Only members with administrator privileges can toggle this")

def setup(bot):
    bot.add_cog(prefix(bot))