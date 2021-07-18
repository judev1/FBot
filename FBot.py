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

class FBot(commands.AutoShardedBot):

    def __init__(self):

        self.SERVER_ID = 717735765936701450
        self.PREMIUM_ID = 815555688520613919

        self.devs = [671791003065384987, 216260005827969024, 311178459919417344, 668423998777982997]

        intents = discord.Intents.none()
        intents.guilds = True
        intents.messages = True
        intents.reactions = True
        #intents.members = True # missing intents

        SHARD_COUNT = 3
        self.shards_ready = 0
        self.ready = False

        super().__init__(command_prefix=fn.getprefix, owner_ids=self.devs, intents=intents,
                         shard_count=SHARD_COUNT)

        self.ftime = fn.ftime()

        self.dbl = dbl.DBLClient(self, os.getenv("TOPGG_TOKEN"), webhook_path="/dblwebhook",
            webhook_auth=os.getenv("WEBHOOK_AUTH"), webhook_port=6000)

        fn.VotingHandler(self)
        self.add_check(self.predicate)

        print("Connecting...\n")

    async def on_shard_ready(self, shard_id):
        print(f" > Shard {shard_id} is ready")

        self.shards_ready += 1
        self.ready = False

        if self.shards_ready == self.shard_count:
            print(f"\n > All shards ready, {self.user} is ready")

            self.ftime.set()
            print(f" > Session started at {bot.ftime.start}\n")

            db.setup()
            db.checkguilds(self.guilds)
            print(" > Setup FBot.db")

            self.premium = await self.get_premium()
            self.cache = cache.Cache(self.devs, self.premium)
            for csv in [tr, cmds]:
                csv.load()

            for command in cm.commands:
                self.cache.cooldowns.add(command, tuple(cm.commands[command][3:5]))
            for command in cm.devcmds:
                self.cache.cooldowns.add(command, (0, 0))
            print(" > Finished setting up cooldowns\n")

            self.remove_command("help")
            for cog in fn.getcogs():
                if cog not in []:
                    print(f"Loading {cog}...", end="")
                    try: self.reload_extension("cogs." + cog[:-3])
                    except: self.load_extension("cogs." + cog[:-3])
                    finally: print("Done")
            print("\n > Finished loading cogs")

            await self.change_presence(status=discord.Status.online,
                                    activity=discord.Game(name="'FBot help'"))

            self.ready = True
            self.shards_ready = 0

    async def get_premium(self):

        guild = self.get_guild(self.SERVER_ID)
        role = guild.get_role(self.PREMIUM_ID)

        premium = set()
        for member in role.members:
            premium.add(member.id)

        return premium

    #async def on_member_update(self, before, after):

    #    if before.roles == after.roles:
    #        return

    #    for role in after.roles:
    #        if role.id == self.PREMIUM_ID:
    #            self.premium.add(after.id)
    #            return

    #    self.premium.remove(after.id)

    def get_colour(self, user_id):
        if user_id in self.premium:
            pass
        return 0xf42f42

    def embed(self, user, title, *desc, url=""):
        colour = self.get_colour(user.id)
        desc = "\n".join(desc)
        return discord.Embed(title=title, description=desc, colour=colour, url=url)

    def predicate(self, ctx):

        user = ctx.author.id
        command = ctx.command.name
        if str(ctx.channel.type) != "private":
            bot_perms = ctx.channel.permissions_for(ctx.guild.get_member(self.user.id))

            valid, perms = [], {}
            for perm in cm.perms[command]:
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
            if cm.commands[command][5] == "*Yes*":
                raise commands.NoPrivateMessage()

        cooldown = self.cache.cooldowns.get(user, command)
        if cooldown:
            self.stats.commands_ratelimited += 1
            raise commands.CommandOnCooldown(commands.BucketType.user, cooldown)
        self.stats.commands_processed += 1
        return True

load_dotenv()
bot = FBot()
bot.run(os.getenv("FBOT_TOKEN"))