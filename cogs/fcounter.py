from discord.ext import commands
from discord import AllowedMentions

class fcounter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        fn, db = bot.fn, bot.db

        @self.bot.event
        async def counter(message):
            try:
                guild_id = message.guild.id
                if db.ignorechannel(guild_id, message.channel.id): return
                if not message.content[0].isdigit(): return
                elif message.author.bot:
                    await message.delete()
                    await message.channel.send("Numbers from bot accounts are not counted")
                elif message.author == self.bot.user: return
                elif message.content == "": return
                elif db.checkdouble(guild_id, message.author.id):
                    text = f"{message.author.mention} ruined it!\nYou can't do two numbers in a row."
                    await message.channel.send(text)
                    await message.add_reaction("❌")
                else:
                    guilds_number = db.getnumber(guild_id)

                    users_number = ""
                    for char in message.content:
                        if char.isdigit(): users_number += char
                        else: break
                    users_number = int(users_number)

                    if users_number != guilds_number + 1:
                        db.resetnumber(guild_id)
                        await message.channel.send(f"{message.author.mention} ruined it!")
                        await message.add_reaction("❌")
                    else:
                        db.updatenumber(users_number, message.author.id, guild_id)
                        db.highscore(users_number, guild_id)

                        await message.add_reaction("✅")
            except: pass

        self.bot.add_listener(counter, "on_message")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload is None: return
        message = payload.cached_message
        if message is None: return
        if message.content.isnumeric():
            last_number = self.bot.db.getnumber(message.guild.id)
            if message.content.startswith(str(last_number)):
                await message.channel.send(f"**The last number in this channel was deleted **\nThe next number is `{last_number+1}`")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):
        if payload is None: return
        message = payload.cached_message
        if message is None: return
        if message.content.isnumeric():
            last_number = self.bot.db.getnumber(message.guild.id)
            if message.content.startswith(str(last_number)):
                await message.channel.send(f"**The last number in this channel was edited**\nThe next number is `{last_number+1}`")

    @commands.command("counting")
    @commands.guild_only()
    async def set_counter_channel(self, ctx):
        if ctx.author.guild_permissions.administrator:
            self.bot.db.setcountingchannel(ctx.channel.id, ctx.guild.id)
            await ctx.send("Set the current channel to counting channel")
        else: await ctx.send("Only administrators can set the counting channel")

    @commands.command("devcounting")
    @commands.is_owner()
    async def dev_set_counter_channel(self, ctx):
        self.bot.db.setcountingchannel(ctx.channel.id, ctx.guild.id)
        await ctx.send("Set current channel to counting channel")

    @commands.command("number",  aliases=["last"])
    async def get_guild_number(self, ctx):
        name = ctx.author.display_name
        last_number = self.bot.db.getnumber(ctx.guild.id)
        try:
            user_id = self.bot.db.getuser(ctx.guild.id)
            last_sender = self.bot.get_user(user_id).name
        except: last_sender = "Nobody"
        embed = self.bot.fn.embed(ctx.author, "FBot counter",
                f"The current number is `{last_number}`, the next is `{last_number + 1}`"
                f"\nLast sender is `{last_sender}`")
        await ctx.send(embed=embed)

    @commands.command("devnumber")
    @commands.is_owner()
    async def _setnumber(self, ctx, *, number):
        if not number.isdigit(): await ctx.send("Not a number")
        else:
            self.bot.db.updatenumber(int(number), ctx.author.id, ctx.guild.id)
            await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(fcounter(bot))

def teardown(bot):
    bot.remove_listener(fcounter, "on_message")