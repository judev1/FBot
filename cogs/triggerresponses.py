from discord.ext import commands
from random import choice
from lib.triggers import tr
import lib.commands as cm
import lib.modes as modes

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

fbot = open("./data/imgs/FBot.png", "rb").read()

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

        if str(message.channel.type) != "private":
            prefix = db.getprefix(message.guild.id)
            db.addchannel(message.channel.id, message.guild.id)
            priority = db.getpriority(message.guild.id)
            mode = db.getmode(message.guild.id)
        else:
            priority = "all"
            prefix = "fbot "
            mode = "default"

        if prefix == "fbot":
            prefix = "fbot "

        if content in [f"<@!{self.bot.user.id}>", f"<@{self.bot.user.id}>"]:
            await send(f"My prefix is `{prefix}`"
                       f"\nUse `{prefix}help` for more help")

        elif str(message.channel.type) == "private" or db.getstatus(message.channel.id) == "on":

            if message.attachments:
                response = choice(responses)
                if mode != "default":
                    response = eval(f"modes.{mode}(response)")
                response = modes.capitalise(response)
                await send(response)
                return

            trigger_detected, response = tr.respond(message, priority)
            if trigger_detected:
                response = response.replace("{username}", name)
                response = response.replace("{answer}", choice(answers))
                response = response.replace("{funny}", choice(funny))
                response = modes.sanitise_text(response)

                if mode != "default":
                    response = eval(f"modes.{mode}(response)")
                modes.capitalise(response)

                if len(response) > 2000:
                    response = response[:1997] + "..."
                await send(response)

def setup(bot):
    bot.add_cog(triggerresponses(bot))