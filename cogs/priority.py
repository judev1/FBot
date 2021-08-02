from discord.ext import commands
import lib.database as db

class Priority(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def respond(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            emoji = self.bot.get_emoji(ctx.author.id)
            if arg == "few":
                db.changepriority(ctx.guild.id, arg)
                await ctx.message.add_reaction(emoji)
            elif arg == "some":
                db.changepriority(ctx.guild.id, arg)
                await ctx.message.add_reaction(emoji)
            elif arg == "all":
                db.changepriority(ctx.guild.id, arg)
                await ctx.message.add_reaction(emoji)
            else:
                await ctx.reply("Respond can only be set to `few`, `some` or `all`")
        else: await ctx.reply("Only members with administrator privileges can toggle this")

def setup(bot):
    bot.add_cog(Priority(bot))