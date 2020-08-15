'''import dbl, asyncio
from discord.ext import commands

class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        webhookurl = "/https://discordapp.com/api/webhooks/724032635453833307/f9cfS4fzfz7py7U-QBIo_ujPc_5CsL2UTEu9nwDV0MtCsdDh6bhRHgq5whLZ0RX7FNZq"
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcxMTkzNDEwMjkwNjk5NDY5OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNTkyNTY4NzM0fQ.Vbv9QxNcvKeACI44jcVvUAPSGNY7mHLcnO1394OgutI"
        self.dblpy = dbl.DBLClient(self.bot, self.token)#, webhook=webhookurl, webhook_auth="FBot")
        
    @commands.command(name="dbl")
    async def _DBL(self, ctx):
        try:
            await self.dblpy.post_guild_count()
            await ctx.send("Posted server count ({})".format(self.dblpy.guild_count()))
        except Exception as e:
            await ctx.send("Failed to post server count\n{}: {}".format(type(e).__name__, e))

    @commands.command(name="bleeeeeeeh")
    async def _toooss(self, ctx):
        voteinfo = await self.dblpy.get_bot_upvotes()
        for votes in voteinfo:
            await print(votes["username"])

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print("Someone voted")
        print(data)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        print(data)
    
def setup(bot):
    bot.add_cog(TopGG(bot))
'''

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjcxMTkzNDEwMjkwNjk5NDY5OSIsImJvdCI6dHJ1ZSwiaWF0IjoxNTkyNTY4NzM0fQ.Vbv9QxNcvKeACI44jcVvUAPSGNY7mHLcnO1394OgutI"

import dbl
import discord
from discord.ext import commands, tasks


class TopGG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = token
        self.dblpy = dbl.DBLClient(self.bot, self.token)

    @tasks.loop(minutes=1.0)
    async def update_stats(self):
        print('Attempting to post server count')
        try:
            await self.dblpy.post_guild_count()
            print('Posted server count ({})'.format(self.dblpy.guild_count()))
        except Exception as e:
            print('Failed to post server count\n{}: {}'.format(type(e).__name__, e))

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print('Received an upvote')
        print(data)

def setup(bot):
    bot.add_cog(TopGG(bot))
