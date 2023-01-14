from discord.ext import commands
import lib.database as db

class Priority(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def respond(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            if arg == "few":
                db.changepriority(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            elif arg == "some":
                db.changepriority(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            elif arg == "all":
                db.changepriority(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            else:
                await ctx.reply("Respond can only be set to `few`, `some` or `all`")
        else: await ctx.reply("Only members with administrator privileges can toggle this")

async def setup(bot):
    await bot.add_cog(Priority(bot))