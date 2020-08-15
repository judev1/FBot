from discord.ext import commands

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="say")
    async def _Say(self, ctx, *message):
        newmessage = ""
        for words in message:
            newmessage += words
        if newmessage != "":
            await ctx.message.delete()
            await ctx.send(message)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))

        
