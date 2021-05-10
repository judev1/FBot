from discord import AllowedMentions
from discord.ext import commands
import modes

class say(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    async def say(self, ctx, inp, filter=None, delete=False):
        inp = " ".join(inp)
        if not inp == "":
            if delete:
                try: await ctx.message.delete()
                except: pass
            try:
                if filter:
                    await ctx.send(filter(inp), allowed_mentions=AllowedMentions.none())
                else:
                    await ctx.send(inp, allowed_mentions=AllowedMentions.none())
            except:
                text = "Text is too long to send"
                if filter:
                    await ctx.send(filter(text))
                else:
                    await ctx.send(text)
        else:
            text = "What do you want me to say!?"
            if filter:
                await ctx.send(filter(text))
            else:
                await ctx.send(text)
        
    @commands.command(name="say")
    async def _Say(self, ctx, *inp):
        await self.say(ctx, inp, delete=True)
        
    @commands.command(name="uwu")
    async def _UWU(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.uwu)
        
    @commands.command(name="confused")
    async def _Confused(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.confused)
        
    @commands.command(name="pirate")
    async def _Pirate(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.pirate)
        
    @commands.command(name="triggered")
    async def _Triggered(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.triggered)
        
    @commands.command(name="italian")
    async def _Italian(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.italian)
        
    @commands.command(name="fuck")
    async def _Fuck(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.fuck)
        
    @commands.command(name="ironic")
    async def _Ironic(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.ironic)
        
    @commands.command(name="patronise")
    async def _Patronise(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.patronise)
        
    @commands.command(name="colonial")
    async def _Colonial(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.colonial)
        
    @commands.command(name="safe")
    async def _Safe(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.safe)
        
    @commands.command(name="biblical")
    async def _Biblical(self, ctx, *inp):
        await self.say(ctx, inp, filter=modes.biblical)

def setup(bot):
    bot.add_cog(say(bot))