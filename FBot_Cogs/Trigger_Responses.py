from discord.ext import commands
from Database import Database as db
from Functions import Functions as fn
from Triggers import trigger_response as tr

remove = fn.Remove
answer = "NO ONE CARES"
tf = ["will", "will not"]

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        name = message.author.display_name
        send = message.channel.send
        content = message.content

        if message.author == self.bot.user or message.author.bot:
            return

        # Checks that a command hasn't been issued
        commandcheck = remove(content, len(fn.Get_Prefix("bot", message)), 0)
        for command in self.bot.walk_commands():
            if commandcheck.startswith(command.name):
                return
            for alias in command.aliases:
                if commandcheck.startswith(alias):
                    return

        # Get prefix
        if message.content.lower() == "prefix":
            prefix = db.Get_Prefix(message.guild.id)
            if prefix == "fbot":
                prefix = "FBot (the default)"
            await send(f"The prefix for this server is `{prefix}`")
        
        # Built-in gifs
        elif message.content.lower() == "smol pp":
            await send("https://tenor.com/view/tiny-small-little-just-alittle-guy-inch-gif-5676598")
            return
        elif message.content.lower() == "micropenis":
            await send("https://tenor.com/view/girl-talks-naughty-small-dick-micropenis-gif-11854548")
            return

        # Coin flipper - feet style
        elif message.content.lower() == "feet pics":
            num = random.randint(0, 1)
            choice = tf[num]
            msg = await send("FBot says:")
            time.sleep(0.5)
            await msg.edit("FBot says:\n(Drum roll please)")
            time.sleep(2)
            await msg.edit(f"FBot says:\n(Drum roll please)\nFeet pics {choice} be granted!")
            return

        # Triggers
        if str(message.channel.type) != "private":
            db.Add_Channel(message.channel.id, message.guild.id)
        if str(message.channel.type) == "private" or db.Get_Status(message.channel.id) == "on":

            if message.attachments:
                await send("That's pretty gay ngl")
                return
            
            trigger_detected, response = tr.trigger_respond(message)
            if trigger_detected:
                response = response.replace("{username}", name)
                response = response.replace("{answer}", answer)
                await send(response)
                return

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
