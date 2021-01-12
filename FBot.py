import discord
import sys
import os

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

token = fn.gettoken(2) # 1 for FBot, 2 for Jude, 3 for Chris

sessionstart = ftime.setstart()
print(f" > Session started at {sessionstart}")

tr.trigger_load()
db.Setup()

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

owners = [671791003065384987, 216260005827969024, 634454757645221908]
bot = commands.Bot(command_prefix=fn.getprefix,
                   owner_ids=owners, intents=intents)

@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")
    db.Check_Guilds(bot.guilds)

    bot.remove_command("help")
    for cog in fn.getcogs():
        cog = cog[0]
        if cog not in ["economy.py", "bigpp.py", "bonk.py", "dbl.py"]: # Cogs not to load
            print(f"Loading {cog}...", end="")
            try: bot.reload_extension("FBot_Cogs." + cog[:-3])
            except: bot.load_extension("FBot_Cogs." + cog[:-3])
            finally: print("Done")
    print(" > Finished loading cogs\n")
        
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="'FBot help'"))

bot.run(token)
