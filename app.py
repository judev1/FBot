import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
import discord
import json
import dbl

from lib.commands import cmds
from lib.triggers import tr
import lib.functions as fn
import lib.commands as cm
import lib.database as db
import lib.cache as cache

class Bot(commands.AutoShardedBot):

    premium = list()

    def __init__(self):

        print(" > Preparing the bot")

        with open("settings.json", "r") as file:
            self.settings = fn.Classify(json.load(file))
            self.devs = self.settings.devs

        intents = discord.Intents.none()
        intents.guilds = True
        intents.messages = True
        intents.reactions = True
        intents.members = True

        super().__init__(
            command_prefix=fn.getprefix,
            intents=intents,
            shard_count=self.settings.shards
        )

        self.shards_ready = [False] * self.shard_count
        self.ftime = fn.ftime()

        self.dbl = dbl.DBLClient(self, self.settings.tokens.topgg, webhook_path="/dblwebhook",
            webhook_auth=self.settings.tokens.auth, webhook_port=self.settings.port)

        fn.VotingHandler(self)
        self.add_check(self.predicate)

        db.setup()
        print("\n > Loaded the database")

        for csv in [tr, cmds]:
            csv.load()

        self.remove_command("help")
        for cog in fn.getcogs():
            if cog not in []:
                print(f"\nLoading {cog}...", end="")
                try: self.reload_extension("cogs." + cog[:-3])
                except: self.load_extension("cogs." + cog[:-3])
                finally: print("Done", end="")
        print("\n\n > Loaded cogs\n")

    def ready(self):
        if all(self.shards_ready):
            if self.is_ready():
                return True
        return False

    async def prep(self):
        print(f"\n > All shards ready, finishing preperations")

        self.ftime.set()
        print(f" > Session started at {self.ftime.start}\n")

        db.checkguilds(self.guilds)

        self.premium = await self.get_premium()
        self.cache = cache.Cache(self.settings.devs, self.premium)

        for command in cm.commands:
            self.cache.cooldowns.add(command, tuple(cm.commands[command][3:5]))
        for command in cm.devcmds:
            self.cache.cooldowns.add(command, (0, 0))
        print(" > Finished setting up cooldowns\n")

        await self.change_presence(status=discord.Status.online,
                                activity=discord.Game(name="'FBot help'"))

        print(f" > Bot is ready")
        self.dispatch("bot_ready")

    async def on_shard_ready(self, shard_id):
        self.shards_ready[shard_id] = True
        ready, shards = sum(self.shards_ready), self.shard_count
        print(f" > Shard {shard_id} CONNECTED, {ready}/{shards} online")

        if self.ready():
            await self.prep()

    async def on_shard_resumed(self, shard_id):
        self.shards_ready[shard_id] = True
        ready, shards = sum(self.shards_ready), self.shard_count
        print(f" > Shard {shard_id} CONNECTED, {ready}/{shards} online")

    async def on_shard_disconnect(self, shard_id):
        if not self.shards_ready[shard_id]:
            self.shards_ready[shard_id] = False
            ready, shards = sum(self.shards_ready), self.shard_count
            print(f" > Shard {shard_id} DISCONNECTED, {ready}/{shards} online")

    async def get_premium(self):

        guild = self.get_guild(self.settings.server)
        role = guild.get_role(self.settings.roles.premium)

        premium = set()
        for member in role.members:
            premium.add(member.id)

        return premium

    def is_premium(self, user_id):
        if user_id in self.premium:
            return True
        return False

    def get_colour(self, user_id):
        if self.is_premium(user_id):
            return db.getcolour(user_id)
        return 0xf42f42

    def get_emoji(self, user_id):
        if self.is_premium(user_id):
            emoji = db.getemoji(user_id)
            if emoji: return emoji
        return "✅"

    def embed(self, user, title, *desc, url=""):
        colour = self.get_colour(user.id)
        desc = "\n".join(desc)
        return discord.Embed(title=title, description=desc, colour=colour, url=url)

    def predicate(self, ctx):

        user = ctx.author.id
        command = ctx.command.name

        if not self.ready():
            return

        if command in cm.devcmds:
            if user not in self.devs:
                raise commands.NotOwner()

        if ctx.command.cog.qualified_name in "Premium":
            if user not in self.devs:
                raise fn.NotPremiumUser()

        if str(ctx.channel.type) != "private":
            bot_perms = ctx.channel.permissions_for(ctx.guild.get_member(self.user.id))

            valid = list()
            perms = dict()
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
                    page += f"{fn.emojis[perms[perm]]} ~ {fn.formatperm(perm)}\n"
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

bot = Bot()
bot.run(bot.settings.tokens.bot)