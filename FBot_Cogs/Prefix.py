import discord
from discord.ext import commands
from Database import Database as db
from Functions import Functions as fn

class FBot_Cogs(commands.Cog):
    
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
                    embed = discord.Embed(title="**Error:** `Prefix too long`", description=f"```Prefixes cannot be longer than '10' characters, yours is {len(arg)}```", colour=0xF42F42)
                    await ctx.send(embed=embed)
                    return
                
                invalid, char = fn.Check_Chars(arg)
                if invalid:
                    embed = discord.Embed(title="**Error:** `Invalid Character`", description=f"```The character ' {char} ' is not allowed```", colour=0xF42F42)
                    await ctx.send(embed=embed)
                else:
                    db.Change_Prefix(ctx.guild.id, arg)
                    await ctx.message.add_reaction("✅")
        else:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
