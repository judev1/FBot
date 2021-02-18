from discord.ext import commands
import discord
import dbl
import sys
import os

sys.path.insert(0, "FBot_Libs")
from functions import fn, ftime
from database import db
from triggers import tr
from commands import cmds
from economy import econ

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

fn = fn()

owners = [671791003065384987, 216260005827969024, 311178459919417344]
bot = commands.Bot(command_prefix=fn.getprefix,
                   owner_ids=owners, intents=intents)
bot.dbl = dbl.DBLClient(bot, fn.gettoken(4), webhook_path="/dblwebhook",
                        webhook_auth=fn.gettoken(5), webhook_port=6000)

fn.bot = bot
bot.fn = fn
bot.db = db()

tr.load()
cmds.load()
econ.load()

bot.ftime = ftime()

print(f" > Session started at {bot.ftime.start}")
token = bot.fn.gettoken(1) # 1 for FBot, 2 for Jude, 3 for Chris

@bot.event
async def on_connect():
    print(f"\n > Began signing into Discord as {bot.user}")

@bot.event
async def on_ready():
    print(f" > Finished signing into Discord as {bot.user}\n")
    bot.db.Check_Guilds(bot.guilds)

    bot.remove_command("help")
    for cog in bot.fn.getcogs():
        if cog not in []: # Cogs not to load
            print(f"Loading {cog}...", end="")
            try: bot.reload_extension("FBot_Cogs." + cog[:-3])
            except: bot.load_extension("FBot_Cogs." + cog[:-3])
            finally: print("Done")
    print("\n > Finished loading cogs\n")
       
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="'FBot help'"))

bot.run(token)
