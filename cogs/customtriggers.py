from discord.ext import commands

import lib.functions as fn

steps = [
    {
        "name": "The Trigger",
        "value": "The trigger is the message or part of the message which "
            "triggers a response. You can use `\` to seperate simmilar "
            "triggers which share the same response.\n"
            "```I am \I'm \Im ```",
        "inline": False
    },
    {
        "name": "The Type",
        "value": "The type determines where in message the trigger will be "
            "looked for. The types include `whole`, `start`, `end`, and "
            "`any`, which are self explanatory. But it also includes "
            "`repeat` which looks for certain repeated characters (indicated "
            "using a '~' like so 'Re~e'), `letters` which looks for messages "
            "which only contain certain letters, and `replace` which will "
            "find a phrase so it can be replaced later.\n"
            "```start```",
        "inline": False
    },
    {
        "name": "The Case",
        "value": "The case specifies whether the trigger has to match the "
            "`exact` case or `any` case\n"
            "```any```",
        "inline": False
    },
    {
        "name": "The Response",
        "value": "The response is the message which FBot replies with. It "
            "inclues special variables such as `{username}` which is "
            "replaced with the trigger-er's name , `{after}` which "
            "includes the rest of the message after 'the trigger', and "
            "`{message}` which contains the original message.\n"
            "```Hi {after}, I'm FBot```",
        "inline": False
    },
    {
        "name": "The Priority",
        "value": "When a server sets the priority to `few`, `some` or `all` "
            "(depending on how much spam they want) this corresponds to what "
            "triggers are called. If your trigger responds to messages "
            "frequently, it should go under `all`> If it responds "
            "infrequently then it should go under `few`.\n"
            "```all```",
        "inline": False
    },
    {
        "name": "Public/Private",
        "value": "If you want your trigger to be publically available, as in "
            "other people can browse triggers and select and use your ones, "
            "choose `public`. If you only want the triggers to be selected "
            "and used by yourself (in the servers you're in), then choose "
            "`private`."
            "```public```",
        "inline": False
    }
]

types = [
    "whole",
    "start",
    "end",
    "any",
    "repeat",
    "letters",
    "replace"
]

class CustomTriggers(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def triggerhelp(self, ctx):
        embed = self.bot.embed(
            ctx.author,
            "How to make a custom trigger",
            "So you wanna make a custom trigger? Follow the steps below to get "
            "started."
        )

        for step in steps:
            embed.add_field(**step)

        await ctx.send(embed=embed)

    @commands.command()
    async def newtrigger(self, ctx):
        choices = list()

        def check(m):
            user = m.author == ctx.author
            channel = m.channel == ctx.channel
            return user and channel

        for i, step in enumerate(steps):
            embed = self.bot.embed(
                ctx.author,
                f"New Custom Trigger - Step {i+1}/{len(steps)}",
                "Type 'CANCEL' to end at any time"
            )

            embed.add_field(**step)
            await ctx.send(embed=embed)

            while True:
                msg = await self.bot.wait_for("message", check=check)

                if msg.content == "CANCEL":
                    await ctx.reply("Cancelled operation")
                    return

                if step["name"] == "The Trigger":
                    choices.append(msg.content)
                elif step["name"] == "The Type":
                    if msg.content.lower() not in types:
                        await msg.reply("Not a valid type, try again")
                        continue
                    choices.append(msg.content.lower())
                elif step["name"] == "The Case":
                    if msg.content.lower() not in ["any", "exact"]:
                        await msg.reply("Not a valid case, try again")
                        continue
                    choices.append(msg.content.lower())
                elif step["name"] == "The Response":
                    choices.append(msg.content)
                elif step["name"] == "The Priority":
                    if msg.content.lower() not in ["few", "some", "all"]:
                        await msg.reply("Not a valid priority, try again")
                        continue
                    choices.append(msg.content.lower())
                elif step["name"] == "Public/Private":
                    if msg.content.lower() not in ["public", "private"]:
                        await msg.reply("Not a valid choice, try again")
                        continue
                    choices.append(msg.content.lower())
                await msg.add_reaction("✅")
                break

        embed = self.bot.embed(
            ctx.author,
            "Created a new trigger with the following settings:"
        )

        for step, choice in zip(steps, choices):
            embed.add_field(name=step["name"], value=f"```{choice}```")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CustomTriggers(bot))