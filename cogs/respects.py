from discord.ext import commands
import asyncio

ongoing_respects = set()

class respects(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="respects")
    async def respects(self, ctx, *args):

        name = " ".join(args)

        # Check there is not an ongoing respect in same channel
        if ctx.channel.id in ongoing_respects:
            msg = await ctx.send("**A respect is already in progress, take a chill pill, and pay your respects you pagan.**")
            await asyncio.sleep(3)
            try:
                await msg.delete()
            except: pass # message might have been deleted
            return
        
        if len(args) != 0:
            ongoing_respects.add(ctx.channel.id)
            m = await ctx.send(f"We gather here to pay respects to **{name}**")
            await m.add_reaction("🇫")
            self.respects_message_id = m.id
        else:
            await ctx.reply("NONONO! Provide some text and try again, you silly sausage.")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, payload):

        emojis = ["🇫"]

        if reaction.message.id != self.respects_message_id: #if a user reacts to any message that isn't the 'respects' message the bot sent above.
            return
        
        if payload.bot: #if the reacting user is a bot
            return

        if reaction.emoji not in emojis: #if a user adds a reaction that isn't the 'F' emoji.
            return

        await reaction.message.channel.send(f"{payload.mention} has payed their respects!") #simply send a message recognising 
            
    
def setup(bot):
    bot.add_cog(respects(bot))