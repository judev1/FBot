import discord
from discord.ext import commands

class ban(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name='ban')
    @commands.is_owner()
    async def ban(ctx, self, member: discord.Member):
        await member.ban()
        await ctx.send("Done")

def setup(bot):
    bot.add_cog(ban(bot))
