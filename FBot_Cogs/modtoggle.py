from discord.ext import commands

class modtoggle(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="modtoggle")
    @commands.guild_only()
    async def _Modtoggle(self, ctx, arg):
        db = self.bot.db
        
        if ctx.author.guild_permissions.administrator:
            if arg in {"on", "off"}:
                db.Change_Modtoggle(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            else:
                embed = self.bot.fn.errorembed("Invalid Argument",
                        f"Modtoggle only accepts 'on' and 'off'")
                await ctx.send(embed=embed)
        else:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(modtoggle(bot))
