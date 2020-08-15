import discord
from discord.ext import commands
from Database import Database as db

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="modtoggle")
    @commands.guild_only()
    async def _Modtoggle(self, ctx, arg):
        name = ctx.author.display_name
        
        if ctx.author.guild_permissions.administrator:
            if arg == "on":
                db.Change_Modtoggle(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            elif arg == "off":
                db.Change_Modtoggle(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            else:
                embed = discord.Embed(title="**Error:** Invalid Argument", description=f"Modtoggle only accepts `'on'` and `'off'`", colour=0xF42F42)
                await ctx.send(embed=embed)
        else:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
