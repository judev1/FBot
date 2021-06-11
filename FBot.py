import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
import discord
import dbl
import os
from dotenv import load_dotenv
load_dotenv()

from lib.functions import fn, ftime, voting_handler, predicate
from lib.database import db
from lib.triggers import tr
from lib.commands import cmds

import lib.commands as cm

fn = fn()

class FBot(commands.Bot):

    def __init__(self):

        owners =  [671791003065384987, 216260005827969024, 311178459919417344, 668423998777982997]

        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False

        super().__init__(command_prefix=fn.getprefix, owner_ids=owners, intents=intents)

        self.fn = fn
        self.db = db()
        self.ftime = ftime()
        self.dbl = dbl.DBLClient(self, os.getenv("TOPGG_TOKEN"), webhook_path="/dblwebhook",
            webhook_auth=os.getenv("WEBHOOK_AUTH"), webhook_port=6000)

        tr.load()
        cmds.load()

    async def on_connect(self):
        print(f"\n > Began signing into Discord as {self.user}")

    async def on_ready(self):
        print(f" > Finished signing into Discord as {self.user}\n")
        self.db.checkguilds(self.guilds)
        fn.setbot(self)
        self.ftime.set()
        print(f" > Session started at {bot.ftime.start}\n")

        self.remove_command("help")
        for cog in self.fn.getcogs():
            if cog not in []:
                print(f"Loading {cog}...", end="")
                try: self.reload_extension("cogs." + cog[:-3])
                except: self.load_extension("cogs." + cog[:-3])
                finally: print("Done")
        print("\n > Finished loading cogs")

        for command in cm.commands:
            self.cache["Cooldowns"].add_command(command, tuple(cm.commands[command][3:5]))
        for command in cm.devcmds:
            self.cache["Cooldowns"].add_command(command, (0, 0))
        print(" > Finished setting up cooldowns\n")

        await self.change_presence(status=discord.Status.online,
                                activity=discord.Game(name="'FBot help'"))

bot = FBot()
voting_handler(bot)

bot.add_check(predicate)
bot.run(os.getenv("JUDE_TOKEN"))