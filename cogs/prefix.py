from discord.ext import commands

class Prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            if arg == "reset":
                await self.bot.db.changeprefix(ctx.guild.id, "fbot")
                await ctx.message.add_reaction("✅")
            else:
                if arg.startswith(("'", '"')) or arg.endswith(("'", '"')):
                    arg = arg[1:-1]
                if len(arg) > 10:
                    await ctx.reply("Prefixes cannot be longer than 10 characters")
                else:
                    await self.bot.db.changeprefix(ctx.guild.id, arg)
                    await ctx.message.add_reaction("✅")
                    await ctx.reply(f"Use `{arg}help` or {self.bot.user.mention} if you get stuck")
            return

        await ctx.reply("Only members with administrator privileges can toggle this")

async def setup(bot):
    await bot.add_cog(Prefix(bot))