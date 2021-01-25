from discord.ext import commands
import discord
import sys
import os

sys.path.insert(0, "FBot_Libs")
from functions import fn, ftime
from database import db
from triggers import tr

# TODO
# REPLACE DEFAULT VALUE FOR JOBS FROM 'None' TO 'Unemployed'
# MULTIPLIER FOR DMs
# LEADERBOARDS
# REMOVE CASE SENSITIVITY

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

fn = fn()

owners = [671791003065384987, 216260005827969024, 311178459919417344]
bot = commands.Bot(command_prefix=fn.getprefix,
                   owner_ids=owners, intents=intents)

bot.fn = fn
bot.db = db()
tr.trigger_load()
bot.ftime = ftime()

token = bot.fn.gettoken(1) # 1 for FBot, 2 for Jude, 3 for Chris

print(f" > Session started at {bot.ftime.start}")

@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")
    bot.db.Check_Guilds(bot.guilds)

    bot.remove_command("help")
    for cog in bot.fn.getcogs():
        if cog not in ["economy.py"]: # Cogs not to load
            print(f"Loading {cog}...", end="")
            try: bot.reload_extension("FBot_Cogs." + cog[:-3])
            except: bot.load_extension("FBot_Cogs." + cog[:-3])
            finally: print("Done")
    print("\n > Finished loading cogs\n")
       
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="'FBot help'"))

bot.run(token)
