from discord.ext import commands
import lib.database as db

joinmsg = ["**Whoa new server, cooooool!**",
           "Thanks for choosing FBot, here are some helpful tips and tricks to get you started",

           ":face_with_symbols_over_mouth: **How do I turn on FBot's spamming/message response feature?**",
           "You can turn this on by using the command `fbot on` (it's case insensitive) in the desired channel and FBot will begin __replying__ to your messages. If only want admins to be able to toggle FBot, you can use `fbot modtoggle on`",

           ":thinking: **How can I set up a counting channel with FBot?**",
           "In the desired channel, use `fbot set` and simply start counting! The rules are simple: send the next number, and don't send two numbers in a row. You can check your highscore, the current number and more with `fbot counting`",

           ":face_with_spiral_eyes: **I'm seeing *way too much* FBot, how can I chill it a bit?**",
           "If you want FBot to respond to less messages you can use `fbot respond few`, by default fbot respond is set to `all`, but you can change it to few, some or all, depending on what suits your server",

           ":zany_face: **That's great and all but are there any other fun features?**",
           "So. Fricken. Many. Image comamnds like `fbot god`, say commands like `fbot biblical`; where you can provide text or reply to a message, same goes for `fbot respects` which is used to pay respects, we've got minigames like `fbot snake`. And so, so much more!",

           ":sleeping: **Sounds great! There can't be anything else, can there?**",
           "Well yes, there is but you'll have to find it out for yourself, with `fbot help` & `fbot cmds`, which will give you a list of commands! And if you find a bug, have a suggestion or just wanna chat, use `fbot server` to enter ~~hell~~ our server!"]

class fakeuser: id = 0
user = fakeuser()

class JoinLeave(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.serverlogs = self.bot.get_channel(720923733132312587)
        self.joinmsg = joinmsg

    @commands.Cog.listener()
    async def on_guild_join(self, newguild):
        db.addguild(newguild.id)

        system_channel = newguild.system_channel
        if system_channel:
            bot_perms = system_channel.permissions_for(newguild.get_member(self.bot.user.id))

            if bot_perms.send_messages:
                embed = self.bot.embed(user, joinmsg[0], joinmsg[1])
                for i in range(2, 11, 2):
                    embed.add_field(name=joinmsg[i], value=joinmsg[i+1], inline=False)
                await system_channel.send(embed=embed)

        memcount = newguild.member_count
        embed = self.bot.embed(user, f"**Added** to `{newguild}`",
                                  str(newguild.id))
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name="Member count", value=f"`{memcount - 1}`")
        await self.serverlogs.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, oldguild):
        db.removeguild(oldguild.id)

        memcount = oldguild.member_count
        embed = self.bot.embed(user, f"**Removed** from `{oldguild}`",
                                  str(oldguild.id))
        embed.add_field(name="Server count", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name="Member count", value=f"`{memcount - 1}`")
        await self.serverlogs.send(embed=embed)

def setup(bot):
    bot.add_cog(JoinLeave(bot))