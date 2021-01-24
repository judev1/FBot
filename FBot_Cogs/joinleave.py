from discord.ext import commands

class joinleave(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.serverlogs = self.bot.get_channel(720923733132312587)
        
    @commands.Cog.listener()
    async def on_guild_join(self, newguild):
        self.bot.db.Add_Guild(newguild.id)

        memcount = newguild.member_count
        #memcount, botcount = 0, 0
        #for member in newguild.members:
        #    if not member.bot:memcount += 1
        #    else: botcount += 1
        
        #try: invite = await newguild.system_channel.create_invite(max_age=
        #    120 * 60, temporary=True)
        #except: invite = "error resolving invite"

        embed = self.bot.fn.embed(f"**Added** to `{newguild}`", newguild.id)
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds) - 1}`")
        embed.add_field(name="Member count", value=f"`{memcount}`")
        #embed.add_field(name="Bot count", value=f"`{botcount - 1}`")
        #embed.add_field(name="Two hour temp invite", value=f"`{invite}`")
        await self.serverlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, oldguild):
        self.bot.db.Remove_Guild(oldguild.id)

        memcount = oldguild.member_count
        #memcount, botcount = 0, 0
        #for member in oldguild.members:
        #    if not member.bot:memcount += 1
        #    else: botcount += 1
        
        embed = self.bot.fn.embed(f"**Removed** from `{oldguild}`", oldguild.id)
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds) - 1}`")
        embed.add_field(name="Member count", value=f"`{memcount}`")
        #embed.add_field(name="Bot count", value=f"`{botcount}`")
        await self.serverlogs.send(embed=embed)

def setup(bot):
    bot.add_cog(joinleave(bot))
