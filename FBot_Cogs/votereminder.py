from discord.ext import tasks, commands

class fakeuser: id = 0
user = fakeuser

class votereminder(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.vote_channel = self.bot.get_channel(808084396900614154)
        self.fbot_general = self.bot.get_channel(717735765936701454)
        
##        self.vote_channel = self.bot.get_channel(727320090483359844)
##        self.fbot_general = self.vote_channel
        # ^ for fbot 3 testing
        self.vote_reminder.start()
        self.is_first_message = True

    @commands.command(name="votereminder")
    @commands.is_owner()
    async def manual_votereminder(self, ctx):
        await ctx.send(embed=self.get_votereminder_embed(ctx.author))

    def get_votereminder_embed(self, user=None):
        if user is None:
            user = fakeuser
        fn = self.bot.fn
        return fn.embed(user,
                        "Vote 4 fbot xd",
                        "You can [vote](https://top.gg/bot/711934102906994699/vote) every 12 hours and earn MAD FBUX",
                        url=fn.votetop)
    #"(https://top.gg/bot/711934102906994699/vote)",

    def cog_unload(self):
        self.vote_reminder.cancel()
    
    @tasks.loop(hours = 12.0)
    async def vote_reminder(self):
        if self.is_first_message:
            self.is_first_message = False
            return
        embed = self.get_votereminder_embed()
        await self.vote_channel.send(embed=embed)
        await self.fbot_general.send(embed=embed)
        
def setup(bot):
    bot.add_cog(votereminder(bot))
