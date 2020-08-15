import discord
from discord.ext import commands
from Database import Database as db
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="respond")
    @commands.guild_only()
    async def _Priority(self, ctx, *, arg):
        name = ctx.author.display_name
        
        if ctx.author.guild_permissions.administrator:
            if arg == "few":
                db.Change_Priority(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            elif arg == "some":
                db.Change_Priority(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            elif arg == "all":
                db.Change_Priority(ctx.guild.id, arg)
                await ctx.message.add_reaction("✅")
            else:
                embed = discord.Embed(title="**Error:** Invalid Argument", description=f"Respond only takes `few`, `some` and `all`", colour=0xF42F42)
                await ctx.send(embed=embed)
        else:
            await ctx.send("NO. NO YOU MAY NOT TOGGLE THAT NON-ADMIN, SHOO")

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
