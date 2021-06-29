from discord.ext import commands

class modtoggle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="modtoggle")
    async def _Modtoggle(self, ctx, arg):
        db = self.bot.db

        if ctx.author.guild_permissions.administrator:
            if arg in {"on", "off"}:
                db.changemodtoggle(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            else:
                embed = self.bot.fn.errorembed("Invalid Argument",
                        f"Modtoggle only accepts 'on' and 'off'")
                await ctx.send(embed=embed)
        else:
            await ctx.reply("Only members with administrator privileges can toggle this")

def setup(bot):
    bot.add_cog(modtoggle(bot))