import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
from dotenv import load_dotenv
from lib.commands import cmds
from lib.triggers import tr
import lib.functions as fn
import lib.commands as cm
import lib.database as db
import lib.cache as cache
import discord
import dbl
import os

emojis = {True: "✅", False: "⛔"}

class FBot(commands.Bot):

    def __init__(self):

        owners =  [671791003065384987, 216260005827969024, 311178459919417344, 668423998777982997]

        intents = discord.Intents.default()
        intents.typing = False
        intents.presences = False

        super().__init__(command_prefix=fn.getprefix, owner_ids=owners, intents=intents)

        db.setup()
        print(" > Setup FBot.db")

        self.cache = dict()
        self.cache["Cooldowns"] = cache.Cooldowns()
        self.cache["Names"] = cache.Names()

        self.ftime = fn.ftime()

        self.dbl = dbl.DBLClient(self, os.getenv("TOPGG_TOKEN"), webhook_path="/dblwebhook",
            webhook_auth=os.getenv("WEBHOOK_AUTH"), webhook_port=6000)

        tr.load()
        cmds.load()

    async def on_connect(self):
        print(f"\n > Began signing into Discord as {self.user}")

    async def on_ready(self):
        print(f" > Finished signing into Discord as {self.user}\n")
        db.checkguilds(self.guilds)
        self.ftime.set()
        print(f" > Session started at {bot.ftime.start}\n")

        self.remove_command("help")
        for cog in fn.getcogs():
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

def predicate(ctx):
    if str(ctx.channel.type) != "private":
        bot_perms = ctx.channel.permissions_for(ctx.guild.get_member(bot.user.id))

        valid, perms = [], {}
        for perm in cm.perms[ctx.command.name]:
            if not perm.startswith("("):
                bot_perm = getattr(bot_perms, perm)
            else: bot_perm = True
            valid.append(bot_perm)
            perms[perm] = bot_perm

        if not all(valid):
            page = "**Missing Permissions**\n\n"
            for perm in perms:
                if perm.startswith("("):
                    perms[perm] = getattr(bot_perms, perm[1:-1])
                page += f"{emojis[perms[perm]]} ~ {fn.formatperm(perm)}\n"
            raise commands.CheckFailure(message=page)
    else:
        if cm.commands[ctx.command.name][5] == "*Yes*":
            raise commands.NoPrivateMessage()

    cooldown = bot.cache["Cooldowns"].cooldown(ctx)
    if cooldown:
        bot.stats.commands_ratelimited += 1
        raise commands.CommandOnCooldown(commands.BucketType.user, cooldown)
    bot.stats.commands_processed += 1
    return True

load_dotenv()

bot = FBot()
fn.VotingHandler(bot)
bot.add_check(predicate)
bot.run(os.getenv("FBOT_TOKEN"))