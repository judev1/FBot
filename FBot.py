import discord
import sys
import os

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

try:
    sys.path.insert(0, "FBot_Libs")
    from database import db
    from discord.ext import commands
    from functions import fn
    from functions import ftime
    from triggers import tr
except Exception as e:
    input(f" > Unable to install some of the dependencies:\n\n{e}\n")
    sys.exit()

# 1 for FBot, 2 for Jude, 3 for Chris
token = fn.gettoken(1)

# Setup
sessionstart = ftime.setstart()
print(f" > Session started at {sessionstart}")
tr.trigger_load()
db.Setup()

owners = [671791003065384987, 216260005827969024, 634454757645221908]
bot = commands.Bot(command_prefix=fn.getprefix, owner_ids=owners, intents=intents)

# When the Bot connects to the server
@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

# When the Server connection is ready
@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")
    db.Check_Guilds(bot.guilds)

    bot.remove_command("help")
    for cog in fn.getcogs():
        cog = cog[0]
        if cog not in ["economy.py", "ppsize"]:
            try: bot.reload_extension("FBot_Cogs." + cog[:-3])
            except: bot.load_extension("FBot_Cogs." + cog[:-3])
    print(" > Loaded all cogs\n")
        
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="'FBot help'"))

bot.run(token)
