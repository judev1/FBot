from discord.ext import commands
from Database import Database as db

serverlogs = 720923733132312587

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_join(self, newguild):
        db.Add_Guild(newguild.id)
        memcount = 0
        botcount = 0
        
        for member in newguild.members:
            if not member.bot:
                memcount += 1
            else:
                botcount += 1
        
        try:
            invite = await newguild.system_channel.create_invite(max_age=120 * 60, temporary=True)
        except:
            invite = "error resolving invite"

        channel = self.bot.get_channel(serverlogs)
        await channel.send(f"I have been `added` to `{newguild}` (`{newguild.id}`)\n"
                           f"{newguild} has `{memcount}` members and `{botcount - 1}` bots\n"
                           f"A temporary invite `{invite}`, will expire after 2 hours\n"
                           f"The server count is now `{len(self.bot.guilds) - 1}`")

    @commands.Cog.listener()
    async def on_guild_remove(self, newguild):
        db.Remove_Guild(newguild.id)
        memcount = 0
        botcount = 0
        
        for member in newguild.members:
            if not member.bot:
                memcount += 1
            else:
                botcount += 1
        
        channel = self.bot.get_channel(serverlogs)
        await channel.send(f"I have been `added` to `{newguild}` (`{newguild.id}`)\n"
                           f"{newguild} has `{memcount}` members and `{botcount}` bots\n"
                           f"The server count is now `{len(self.bot.guilds) - 1}`")

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
