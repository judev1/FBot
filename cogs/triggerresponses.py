from discord.ext import commands
from lib.triggers import tr
import lib.functions as fn
import lib.commands as cm
import lib.modes as modes
from random import choice

responses = [
    "Someone has bad taste in photos",
    "Your right to live has now been revoked",
    "I wish I hadn't seen that",
    "MY EYES! MY EYES! WHY WOULD YOU SEND THAT!?",
    "Oh my, what have I just witnessed",
    "That be kinda stanky ngl",
    "Spare me, please",
    "I'm not feeling that, delete immediatley",
    "That is not vibe"
]

funny = [
    "Hmm, maybe I'll laugh too next time",
    "HAHAHA, was that the reaction you were looking for?",
    "It would be easier to laugh if it were funny",
    "That is **h i l a r i o u s**",
    "L O L",
    "Wow my dude that is so funny"
]

answers = [
    "Good question",
    "idk",
    "Why are you asking me?",
    "I don't think we'll ever know"
]

class TriggerResponses(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.bot.ready():
            return

        if message.author.bot: return

        name = message.author.display_name
        channel = message.channel
        content = message.content

        if str(message.channel.type) != "private":
            if not message.channel.permissions_for(
                message.guild.get_member(self.bot.user.id)).send_messages:
                return

        prefix = await fn.getprefix(self.bot, message)
        commandcheck = content[len(prefix):]
        for command in cm.commands:
            if commandcheck.startswith(command):
                return
        for command in cm.devcmds:
            if commandcheck.startswith(command):
                return

        if content.lower().startswith("fball"):
            return

        for user in self.bot.userdms:
            if message.author.id == user:
                return

        if str(message.channel.type) != "private":
            prefix = await self.bot.db.getprefix(message.guild.id)
            await self.bot.db.addchannel(message.channel.id, message.guild.id)
            priority = await self.bot.db.getpriority(message.guild.id)
            mode = await self.bot.db.getmode(message.guild.id)
        else:
            priority = "all"
            prefix = "fbot "
            mode = "default"

        if prefix == "fbot":
            prefix = "fbot "

        if content in [f"<@!{self.bot.user.id}>", f"<@{self.bot.user.id}>"]:
            await message.reply(f"My prefix is `{prefix}`. Use `{prefix}help` for more help")

        elif str(message.channel.type) == "private" or await self.bot.db.getstatus(message.channel.id) == "on":

            if message.attachments:
                response = choice(responses)
                if mode != "default":
                    response = eval(f"modes.{mode}(response)")
                response = modes.capitalise(response)
                await channel.send(response)
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
                await channel.send(response)

async def setup(bot):
    await bot.add_cog(TriggerResponses(bot))