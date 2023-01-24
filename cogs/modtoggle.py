from discord.ext import commands

class Modtoggle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def modtoggle(self, ctx, arg):
        if ctx.author.guild_permissions.administrator:
            if arg in {"on", "off"}:
                await self.bot.db.changemodtoggle(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            else:
                await ctx.reply("Modtoggle can only be set to `on` or `off`")
        else:
            await ctx.reply("Only members with administrator privileges can toggle this")

async def setup(bot):
    await bot.add_cog(Modtoggle(bot))