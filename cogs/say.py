from discord import AllowedMentions
from discord.ext import commands
import modes

class say(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    async def say(self, ctx, text, filter=None, delete=False):
        
        text = " ".join(text)
        if not text == "":
            if delete:
                try: await ctx.message.delete()
                except: pass
        else:
            text = "What do you want me to say!?"
        
        if filter:
            text = filter(text)
        text = modes.capitalise(text)
        
        try:
            await ctx.send(text, allowed_mentions=AllowedMentions.none())
        except:
            text = "Text is too long to send"
            if filter:
                text = filter(text)
            text = modes.capitalise(text)
            await ctx.send(text)
        
    @commands.command(name="say")
    async def _Say(self, ctx, *text):
        await self.say(ctx, text, delete=True)
        
    @commands.command(name="uwu")
    async def _UWU(self, ctx, *text):
        await self.say(ctx, text, filter=modes.uwu)
        
    @commands.command(name="confused")
    async def _Confused(self, ctx, *text):
        await self.say(ctx, text, filter=modes.confused)
        
    @commands.command(name="pirate")
    async def _Pirate(self, ctx, *text):
        await self.say(ctx, text, filter=modes.pirate)
        
    @commands.command(name="triggered")
    async def _Triggered(self, ctx, *text):
        await self.say(ctx, text, filter=modes.triggered)
        
    @commands.command(name="italian")
    async def _Italian(self, ctx, *text):
        await self.say(ctx, text, filter=modes.italian)
        
    @commands.command(name="fuck")
    async def _Fuck(self, ctx, *text):
        await self.say(ctx, text, filter=modes.fuck)
        
    @commands.command(name="ironic")
    async def _Ironic(self, ctx, *text):
        await self.say(ctx, text, filter=modes.ironic)
        
    @commands.command(name="patronise")
    async def _Patronise(self, ctx, *text):
        await self.say(ctx, text, filter=modes.patronise)
        
    @commands.command(name="colonial")
    async def _Colonial(self, ctx, *text):
        await self.say(ctx, text, filter=modes.colonial)
        
    @commands.command(name="safe")
    async def _Safe(self, ctx, *text):
        await self.say(ctx, text, filter=modes.safe)
        
    @commands.command(name="biblical")
    async def _Biblical(self, ctx, *text):
        await self.say(ctx, text, filter=modes.biblical)

def setup(bot):
    bot.add_cog(say(bot))