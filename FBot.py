import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
import discord
import dbl
import sys
import os
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, "lib")
from functions import fn, ftime, voting_handler
from database import db
from triggers import tr
from commands import cmds
from economy import econ

import commands as cm

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

fn = fn()

owners = [671791003065384987, 216260005827969024]
bot = commands.Bot(command_prefix=fn.getprefix,
                   owner_ids=owners, intents=intents)

voting_handler(bot)
bot.dbl = dbl.DBLClient(bot, os.getenv("TOPGG_TOKEN"), webhook_path="/dblwebhook",
          webhook_auth=os.getenv("WEBHOOK_AUTH"), webhook_port=6000)

bot.fn = fn
bot.db = db()

tr.load()
cmds.load()
econ.load()

bot.ftime = ftime()

print(f" > Session started at {bot.ftime.start}")
token = os.getenv("FBOT_TOKEN") # 1 for FBot, 2 for Jude, 3 for Chris

@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")
    bot.db.Check_Guilds(bot.guilds)
    fn.setbot(bot)

    bot.remove_command("help")
    for cog in bot.fn.getcogs():
        if cog not in []: # Cogs not to load
            print(f"Loading {cog}...", end="")
            try: bot.reload_extension("cogs." + cog[:-3])
            except: bot.load_extension("cogs." + cog[:-3])
            finally: print("Done")
    print("\n > Finished loading cogs")

    for command in cm.commands:
        bot.cache["Cooldowns"].add_command(command, tuple(cm.commands[command][3:5]))
    for command in cm.devcmds:
        bot.cache["Cooldowns"].add_command(command, (0, 0))
    print(" > Finished setting up cooldowns\n")
       
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="'FBot help'"))

bot.run(token)