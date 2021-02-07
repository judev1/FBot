from discord.ext import tasks, commands

class votereminder(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.vote_channel = self.bot.get_channel(757722305395949572)
        self.fbot_general = self.bot.get_channel(717735765936701454)
        
##        self.vote_channel = self.bot.get_channel(727320090483359844)
##        self.fbot_general = self.vote_channel
        # ^ for fbot 3 testing
        self.vote_reminder.start()
        self.is_first_message = True

    @commands.command(name="votereminder")
    @commands.is_owner()
    async def manual_votereminder(self, ctx):
        await ctx.send(self.get_votereminder())

    def get_votereminder(self):
        fn = self.bot.fn
        msg = "vote 4 fbot xd\n\nhttps://top.gg/bot/711934102906994699/vote"
        return msg

    def cog_unload(self):
        self.vote_reminder.cancel()
    
    @tasks.loop(hours = 12.0)
    async def vote_reminder(self):
        if self.is_first_message:
            self.is_first_message = False
            #return
        msg = self.get_votereminder()
        await self.vote_channel.send(msg)
        await self.fbot_general.send(msg)
        
def setup(bot):
    bot.add_cog(votereminder(bot))
