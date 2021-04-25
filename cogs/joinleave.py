from discord.ext import commands

joinmsg = ["**Whoa new server, cooooool**",
           "Thanks for choosing FBot, here are some helpful tips and tricks to get you started",

           "", ":speech_balloon: **How do I turn on FBot's spamming/message response feature?**",
           "You can turn this on by using the command `fbot on` (don't worry about the case) in the desired channel and FBot will begin replying to your messages. If only want admin to be able to toggle FBot, you can use `fbot modtoggle on` to do this",

           "", ":1234: **How can I set up a counting channel with FBot?**",
           "In the channel which you want to be your counting channel, use `fbot counting` and simply start counting! You can count on it!",

           "", ":sound: **I'm seeing too much FBot how can I calm it down?**",
           "If you want FBot to respond to less messages you can use `fbot respond few`, by default fbot respond is set to `all`, but you can change it to few, some or all, depending on what suits your server",

           "", ":safety_pin: **Anything else?**",
           "Well if you need anything else use `fbot help`, where you can find a list of commands, an invite to our support server, and more!"]

class fakeuser: id = 0
user = fakeuser()

class joinleave(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.serverlogs = self.bot.get_channel(720923733132312587)
        
    @commands.Cog.listener()
    async def on_guild_join(self, newguild):
        self.bot.db.Add_Guild(newguild.id)

        try:
            try:
                embed = self.bot.fn.embed(user, joinmsg[0], joinmsg[1])
                for i in range(3, 16, 3):
                    embed.add_field(name=joinmsg[i], value=joinmsg[i+1],
                                    inline=False)
                await newguild.system_channel.send(embed=embed)
            except:
                await newguild.system_channel.send("\n".join(joinmsg))
        except: pass
                

        memcount = newguild.member_count        
        embed = self.bot.fn.embed(user, f"**Added** to `{newguild}`",
                                  str(newguild.id))
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name="Member count", value=f"`{memcount - 1}`")
        await self.serverlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, oldguild):
        self.bot.db.Remove_Guild(oldguild.id)

        memcount = oldguild.member_count
        embed = self.bot.fn.embed(user, f"**Removed** from `{oldguild}`",
                                  str(oldguild.id))
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name="Member count", value=f"`{memcount - 1}`")
        await self.serverlogs.send(embed=embed)

def setup(bot):
    bot.add_cog(joinleave(bot))