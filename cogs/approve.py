from discord.ext import commands

class approve(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="approve")
    async def _Approve(self, ctx, *args):

        if args:
            msg = ctx.message
        else:
            try: await ctx.message.delete()
            except: pass

            reference = ctx.message.reference
            if reference:
                msg = await ctx.fetch_message(id=reference.message_id)
            else:
                msg = None
        
        await ctx.send("I'm FBot and I approve of this message")#, reference=msg) # Doesn't work for some reason
          
def setup(bot):
    bot.add_cog(approve(bot))