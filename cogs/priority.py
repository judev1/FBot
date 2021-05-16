from discord.ext import commands

class priority(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="respond")
    async def _Priority(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            db = self.bot.db
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
                embed = self.bot.fn.errorembed("Invalid Argument",
                        "Respond only takes `few`, `some` and `all`")
                await ctx.send(embed=embed)
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(priority(bot))