import nest_asyncio
nest_asyncio.apply()

from discord.ext import commands
import discord
import json

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

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix=fn.getprefix, intents=intents,
                         shard_count=self.settings.shards)

        self.shards_connected = 0
        self.shards_ready = list()

        self.prepped = False
        self.bot_ready = False
        self.cleaning = False

    def ready(self):
        return self.bot_ready

    def are_shards_ready(self):
        if len(self.shards_ready) == self.shard_count and not self.cleaning:
            return True
        return False

    async def prep(self):

        self.ftime = fn.ftime()
        self.ftime.set()
        print(f"\n > All shards ready, finishing preparations")
        print(f" > Session started at {self.ftime.start}\n")

        # fn.VotingHandler(self)
        self.add_check(self.predicate)

        self.db = await db.connect(self.settings)
        print(" > Loaded the database")

        for csv in [tr, cmds]:
            csv.load()

        self.remove_command("help")
        for cog in fn.getcogs():
            if cog not in []:
                print(f"\nLoading {cog}...", end="")
                try: await self.reload_extension("cogs." + cog[:-3])
                except: await self.load_extension("cogs." + cog[:-3])
                finally: print("Done", end="")
        print("\n\n > Loaded cogs\n")

        self.premium = await self.get_premium()
        self.cache = cache.Cache(self.settings.devs, self.premium)

        for command in cm.commands:
            self.cache.cooldowns.add(command, tuple(cm.commands[command][3:5]))
        for command in cm.devcmds:
            self.cache.cooldowns.add(command, (0, 0))
        print(" > Finished setting up cooldowns")

        await self.change_presence(status=discord.Status.online,
                                activity=discord.Game(name="'FBot help'"))

        self.prepped = True

    async def cleanup(self):
        c = await self.db.connection(autoclose=False)
        guild_ids = dict()
        for guild in bot.guilds:
            guild_ids[guild.id] = guild

        count = [0, 0]
        for guild in bot.guilds:
            await c.execute("SELECT guild_id FROM guilds WHERE guild_id=%s;", (guild.id,))
            if not await c.fetchone():
                await self.db.addguild(guild.id)
                count[0] += 1
            # doesnt work for some god foresaken reason
            await c.execute("SELECT guild_id FROM counting WHERE guild_id=%s;", (guild.id,))
            result = await c.fetchone()
            if not result:
                await self.db.addcounting(guild.id)
                count[1] += 1
        print("Added", count[0], "guilds to 'guilds'")
        print("Added", count[1], "missing guilds to 'counting'")

        count = [0, 0]
        await c.execute("SELECT guild_id FROM guilds;")
        for row in await c.fetchall():
            guild_id = row[0]
            if not (guild_id in guild_ids):
                await self.db.removeguild(guild_id)
                count[0] += 1
            else:
                channel_ids = [channel.id for channel in guild_ids[guild_id].channels]
                await c.execute("SELECT channel_id FROM channels WHERE guild_id=%s;", (guild_id,))
                for row in await c.fetchall():
                    channel_id = row[0]
                    if not (channel_id in channel_ids):
                        await c.execute("DELETE FROM channels WHERE channel_id=%s;", (channel_id,))
                        count[1] += 1
        print("Removed", count[0], "guilds from 'guilds'")
        print("Removed", count[1], "channels from 'channels'")

        count = 0
        await c.execute("SELECT guild_id FROM channels;")
        for row in await c.fetchall():
            guild_id = row[0]
            if not (guild_id in guild_ids):
                await c.execute("DELETE FROM channels WHERE guild_id=%s;", (guild_id,))
                count += 1
        print("Removed", count, "guild channels from 'channels'")

        count = 0
        await c.execute("SELECT guild_id FROM counting;")
        for row in await c.fetchall():
            guild_id = row[0]
            if not (guild_id in guild_ids):
                await c.execute("DELETE FROM counting WHERE guild_id=%s;", (guild_id,))
                count += 1
        print("Removed", count, "guilds from 'counting'\n")

        await c.close()

        self.cleaning = False
        print(f" > Bot is ready")
        self.dispatch("bot_ready")
        self.bot_ready = True

    async def on_shard_connect(self, shard_id):
        self.shards_connected += 1
        print(f" > Shard {shard_id} CONNECTED, {self.shards_connected}/{self.shard_count} connected")

    async def on_shard_ready(self, shard_id):
        if not shard_id in self.shards_ready:
            self.shards_ready.append(shard_id)
        print(f" > Shard {shard_id} READY, {len(self.shards_ready)}/{self.shard_count} ready")

        if self.are_shards_ready():
            if not self.prepped:
                await self.prep()
            if not self.cleaning:
                self.cleaning = True
                print(" > Cleaning up the database")
                await self.cleanup()

    async def on_shard_resumed(self, shard_id):
        self.shards_connected += 1
        if not shard_id in self.shards_ready:
            self.shards_ready.append(shard_id)
        print(f" > Shard {shard_id} RESUMED, {len(self.shards_ready)}/{self.shard_count} ready")

        if self.are_shards_ready() and not self.cleaning and self.prepped:
            await self.cleanup()

    async def on_shard_disconnect(self, shard_id):
        self.shards_connected -= 1
        if shard_id in self.shards_ready:
            self.shards_ready.remove(shard_id)
        self.bot_ready = False
        print(f" > Shard {shard_id} DISCONNECTED, {len(self.shards_ready)}/{self.shard_count} online")

    async def get_premium(self):

        guild = self.get_guild(self.settings.server)
        role = guild.get_role(self.settings.roles.premium)

        premium = set()
        for member in role.members:
            premium.add(member.id)

        return premium

    #async def on_member_update(self, before, after):

    #    if before.roles == after.roles:
    #        return

    #    for role in after.roles:
    #        if role.id == self.settings.roles.premium:
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

        if not self.ready():
            return

        if command in cm.devcmds:
            if user not in self.devs:
                raise commands.NotOwner()

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
bot.run(bot.settings.tokens.bot, log_level=50)