import discord, os
from BookProgram import book
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars(var1="hitlerurl")
hitlerurl = variables[0]

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="quote")
    async def _Quote(self, ctx):
        
        if os.path.exists('./Mein_Kampf.txt'):
            quote = book.quote()
            embed = discord.Embed(title=quote, colour=0x000000)
            embed.set_footer(text="- Adolf Hitler", icon_url=hitlerurl)
            await ctx.send(embed=embed)
        else:
            await ctx.send("This feature is currently disabled")

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
