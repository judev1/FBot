from discord.ext import commands
from database import db
from functions import fn

class prefix(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="prefix")
    @commands.guild_only()
    async def _ChangePrefix(self, ctx, *, arg):
        if ctx.author.guild_permissions.administrator:
            if arg == "reset":
                db.Change_Prefix(ctx.guild.id, "fbot")
                await ctx.message.add_reaction("✅")
            else:
                name = ctx.author.display_name
                if len(arg) > 10:
                    embed = fn.errorembed("Prefix too long", f"Prefixes cannot be longer than '10' characters, yours is {len(arg)}")
                    await ctx.send(embed=embed)
                    return
                
                invalid, char = fn.checkchars(arg)
                if invalid:
                    embed = dn.errormbed("Invalid Character", f"The character ' {char} ' is not allowed")
                    await ctx.send(embed=embed)
                else:
                    db.Change_Prefix(ctx.guild.id, arg)
                    await ctx.message.add_reaction("✅")
        else: await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(prefix(bot))
