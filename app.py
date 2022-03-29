import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
import discord
import json
import dbl
import asyncio

from lib.commands import cmds
from lib.triggers import tr
import lib.functions as fn
import lib.commands as cm
import lib.database as db
import lib.cache as cache

def temp():
    import sqlite3
    import os

    print("ALERT: This method is to be used to migrate the database. It is to be used ONCE. Below is a temp() call that runs this function, once this function is run, replace the call with db.setup()")
    asyncio.sleep(5)

    os.rename("./data/FBot.db", "./data/OLD.db")

    db.setup()
    old_c = sqlite3.connect("./data/OLD.db").cursor()

    old_c.execute("""SELECT guild_id, notice,
                            prefix, modtoggle, priority, mode FROM guilds;""")
    for data in old_c.fetchall():
        db.update("""
            INSERT INTO guilds (
                guild_id, notice,
                prefix, modtoggle, priority, mode, language,
                name, picture, custom_commands,
                commands, triggers, joined, removed
            ) VALUES (
                ?, ?,
                ?, ?, ?, ?, 'english',
                '', '', '[]',
                0, 0, 0, 0
            )""", data)

    old_c.execute("SELECT guild_id, channel_id, status FROM channels;")
    for data in old_c.fetchall():
        db.update("""
            INSERT INTO channels (
                guild_id, channel_id, status, shout
            ) VALUES (
                ?, ?, ?, 'no'
            )""", data)

    old_c.execute("SELECT user_id, ppsize, commands, triggers FROM users;")
    for data in old_c.fetchall():
        db.update(f"""
            INSERT INTO users (
                user_id, ppsize,
                commands, triggers,
                expiry, title, colour, emoji, say, delete_say,
                claims, custom_triggers
            ) VALUES (
                ?, ?,
                ?, ?,
                0, '', {0xf42f42}, '', 'fbot', 'no', 0, 0
            )""", data)

    old_c.execute("SELECT * FROM counting;")
    for data in old_c.fetchall():
        db.update("""
            INSERT INTO counting (
                guild_id, channel_id, number, user_id, record
            ) VALUES (
                ?, ?, ?, ?, ?
            )""", data)

    old_c.execute("SELECT user_id, topvotes, total_topvotes, last_topvote FROM votes;")
    for data in old_c.fetchall():
        db.update("""
            INSERT INTO topvotes (
                    user_id, votes, total_votes, last_vote
                ) VALUES (
                    ?, ?, ?, ?,
                )""", data)

    old_c.execute("SELECT user_id, dblvotes, total_dblvotes, last_dblvote FROM votes;")
    for data in old_c.fetchall():
        db.update("""
            INSERT INTO dblvotes (
                user_id, votes, total_votes, last_vote
            ) VALUES (
                ?, ?, ?, ?,
            );""", data)

    old_c.execute("SELECT user_id, bfdvotes, total_bfdvotes, last_bfdvote FROM votes;")
    for data in old_c.fetchall():
        db.update("""
            INSERT INTO bfdvotes (
                user_id, votes, total_votes, last_vote
            ) VALUES (
                ?, ?, ?, ?,
            )""", data)

class Bot(commands.AutoShardedBot):

    premium = list()

    def __init__(self):

        print(" > Preparing the bot")

        with open("settings.json", "r") as file:
            self.settings = fn.Classify(json.load(file))
            self.devs = self.settings.devs

        intents = discord.Intents.all()
        intents.presences = False
        intents.bans = False
        intents.integrations = False
        intents.typing = False
        intents.webhooks = False
        intents.invites = False
        intents.members = False
        # This is a hotfix to allow for local development of the bot, while keeping the integrity of the production bot up and making sure it doesn't crash. It will get a proper fix soon(tm)

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

        temp() # db.setup()
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

        self.cache = cache.Cache(self.settings.devs)
        self.update_premium()

        for command in cm.commands:
            self.cache.cooldowns.add(command, tuple(cm.commands[command][3:5]))
        for command in cm.devcmds:
            self.cache.cooldowns.add(command, (0, 0))
        print(" > Finished setting up cooldowns\n")

        await self.change_presence(status=discord.Status.online,
                                activity=discord.Game(name="'FBot help'"))

        print(f" > Bot is ready\n")
        self.dispatch("bot_ready")

    async def on_disconnect(self):
        self.shards_ready = [False]*3

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

    def update_premium(self):
        for user_id, expiry in db.getallpremium():
            self.cache.premium.add(user_id, True, expiry)

    def is_premium(self, user_id):
        if self.cache.premium.get(user_id):
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
            if not self.is_premium(user):
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