from discord.ext import commands
from database import db
from functions import fn

serverlogs = 720923733132312587

class joinleave(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_guild_join(self, newguild):
        db.Add_Guild(newguild.id)

        memcount, botcount = 0, 0
        for member in newguild.members:
            if not member.bot:memcount += 1
            else: botcount += 1
        
        try: invite = await newguild.system_channel.create_invite(max_age=
            120 * 60, temporary=True)
        except: invite = "error resolving invite"

        channel = self.bot.get_channel(serverlogs)
        embed = fn.embed(f"Added to `{newguild}`", newguild.id)
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds) - 1}`")
        embed.add_field(name="Member count", value=f"`{memcount}`")
        embed.add_field(name="Bot count", value=f"`{botcount - 1}`")
        embed.add_field(name="Two hour temp invite", value=f"`{invite}`")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, oldguild):
        db.Remove_Guild(oldguild.id)

        memcount, botcount = 0, 0
        for member in oldguild.members:
            if not member.bot:memcount += 1
            else: botcount += 1
        
        channel = self.bot.get_channel(serverlogs)
        embed = fn.embed(f"Removed from `{oldguild}`", oldguild.id)
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds) - 1}`")
        embed.add_field(name="Member count", value=f"`{memcount}`")
        embed.add_field(name="Bot count", value=f"`{botcount}`")
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(joinleave(bot))
