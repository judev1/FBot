from discord.ext import commands
import lib.database as db

class Modtoggle(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def modtoggle(self, ctx, arg):
        if ctx.author.guild_permissions.administrator:
            if arg in {"on", "off"}:
                db.changemodtoggle(ctx.guild.id, arg)
                emoji = self.bot.get_emoji(ctx.author.id)
                await ctx.message.add_reaction(emoji)
            else:
                await ctx.reply("Modtoggle can only be set to `on` or `off`")
        else:
            await ctx.reply("Only members with administrator privileges can toggle this")

def setup(bot):
    bot.add_cog(Modtoggle(bot))