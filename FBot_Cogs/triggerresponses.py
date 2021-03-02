from discord.ext import commands
from random import choice
from triggers import tr
import commands as cm
import asyncio

tf = ["will", "will not"]
responses = ["Someone has bad taste in photos",
             "Your right to live has now been revoked",
             "I wish I hadn't seen that",
             "MY EYES! MY EYES! WHY WOULD YOU SEND THAT!?",
             "Oh my, what have I just witnessed",
             "That be kinda stanky ngl",
             "Spare me, please",
             "I'm not feeling that, delete immediatley",
             "That is not vibe"]
funny = ["Hmm, maybe I'll laugh too next time",
         "HAHAHA, was that the reaction you were looking for?",
         "It would be easier to laugh if it were funny",
         "That is **h i l a r i o u s**",
         "L O L",
         "Wow my dude that is so funny"]
answers = ["Good question",
           "idk",
           "Why are you asking me?",
           "I don't think we'll ever know"]

class triggerresponses(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot: return

        name = message.author.display_name
        send = message.channel.send
        content = message.content
        db = self.bot.db

        if str(message.channel.type) != "private":
            if not message.channel.permissions_for(
                message.guild.get_member(self.bot.user.id)).send_messages:
                return

        prefix = self.bot.fn.getprefix(self.bot, message)
        commandcheck = content[len(prefix):]
        for command in cm.commands:
            if commandcheck.startswith(command):
                return
        for command in cm.devcmds:
            if commandcheck.startswith(command):
                return

        if content.lower().startswith("fball"):
            return

        if content.lower() == "prefix":
            if not message.guild:
                await send("The prefix for DMs is `FBot `")
                return
            prefix = db.Get_Prefix(message.guild.id)
            if prefix == "fbot":
                await send("The prefix for this server is `fbot ` (the default)")
            else:
                await send(f"The prefix for this server is `{prefix}`")

        elif content.lower() == "smol pp":
            await send("https://tenor.com/view/tiny-small-little-just-alittle-guy-inch-gif-5676598")
            return
        elif content.lower() == "micropenis":
            await send("https://tenor.com/view/girl-talks-naughty-small-dick-micropenis-gif-11854548")
            return

        elif content.lower() == "feet pics":
            msg = await send("FBot says:\n(Drum roll please)")
            await asyncio.sleep(2)
            await msg.edit(content=f"FBot says:\nFeet pics {choice(tf)} be granted!")
            return

        if str(message.channel.type) != "private":
            prefix = db.Get_Prefix(message.guild.id)
            db.Add_Channel(message.channel.id, message.guild.id)
            priority = db.Get_Priority(message.guild.id)
        else: priority, prefix = "all", "fbot"
        if prefix == "fbot": prefix = "fbot "

        if content == f"<@!{self.bot.user.id}>":
            await send(f"My prefix is `{prefix}`"
                       f"\nUse `{prefix}help` for more help")
        elif str(message.channel.type) == "private" or db.Get_Status(message.channel.id) == "on":

            if message.attachments:
                await send(choice(responses))
                return
            
            trigger_detected, response = tr.respond(message, priority)
            if trigger_detected:
                response = response.replace("{username}", name)
                response = response.replace("{answer}", choice(answers))
                response = response.replace("{funny}", choice(funny))
                if len(response) > 2000:
                    response = response[:2000]
                await send(response)

def setup(bot):
    bot.add_cog(triggerresponses(bot))
