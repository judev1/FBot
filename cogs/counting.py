from discord.ext import commands

cares = (" ✅ When a message is deleted\n"
         " ✅ When a message is edited\n"
         " ✅ When a fake reaction is added\n"
         " ❌ Non-counting messages\n"
         " ❌ Trailing text after numbers")

def clean(content):
    number = ""
    for char in content:
        if char.isdigit(): number += char
        else: break
    return int(number)

class Counting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if not self.bot.ready():
            return

        try:
            guild_id = message.guild.id

            if message.channel.id != await self.bot.db.getcountingchannel(guild_id):
                return
            elif not message.content[0].isdigit():
                return
            elif message.content == "":
                return

            guilds_number = await self.bot.db.getnumber(guild_id)

            if message.author.bot:
                await message.channel.send(f"Numbers from bot accounts are not counted. The next number is `{guilds_number+1}`")
            elif message.author.id == await self.bot.db.getuser(guild_id):
                await self.bot.db.resetnumber(guild_id)
                await message.add_reaction("❌")
                await message.channel.send(f"{message.author.mention} ruined it! You can't do two numbers in a row")
            else:
                users_number = clean(message.content)

                if users_number != guilds_number + 1:
                    await self.bot.db.resetnumber(guild_id)
                    await message.add_reaction("❌")
                    await message.channel.send(f"{message.author.mention} ruined it!")
                else:
                    await self.bot.db.updatenumber(users_number, message.author.id, guild_id)
                    await message.add_reaction("✅")
                    if str(users_number).endswith("69"):
                        await message.add_reaction("👌")
                    elif users_number == 100:
                        await message.add_reaction("💯")
        except: pass

    @commands.command()
    async def set(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await self.bot.db.setcountingchannel(ctx.channel.id, ctx.guild.id)
            await ctx.reply("Set the current channel to counting channel")
        else:
            await ctx.reply("Only administrators can set the counting channel")

    @commands.command()
    async def remove(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await self.bot.db.removecountingchannel(ctx.guild.id)
            await ctx.reply("Removed the counting channel")
        else:
            await ctx.reply("Only administrators can remove the counting channel")

    @commands.command()
    async def devset(self, ctx):
        await self.bot.db.setcountingchannel(ctx.channel.id, ctx.guild.id)
        await ctx.send("Set current channel to counting channel")

    @commands.command()
    async def devremove(self, ctx):
        await self.bot.db.removecountingchannel(ctx.guild.id)
        await ctx.send("Removed the counting channel")

    @commands.command()
    async def counting(self, ctx):

        embed = self.bot.embed(ctx.author, "FBot counting")

        last_number = await self.bot.db.getnumber(ctx.guild.id)
        embed.add_field(name="Last number", value=last_number)

        user_id = await self.bot.db.getuser(ctx.guild.id)
        try: last_counter = (await self.bot.fetch_user(user_id)).mention
        except: last_counter = "Nobody"
        embed.add_field(name="Last counter", value=last_counter)

        embed.add_field(name="Anti-sabotage detects...", value=cares, inline=False)

        channel_id = await self.bot.db.getcountingchannel(ctx.guild.id)
        try: channel = f"<#{(await self.bot.fetch_channel(channel_id)).id}>"
        except: channel = "None"
        embed.add_field(name="Channel", value=channel)

        highscore = await self.bot.db.gethighscore(ctx.guild.id)
        embed.add_field(name="Highscore", value=highscore)

        await ctx.send(embed=embed)

    @commands.command()
    async def setnumber(self, ctx, *, number):
        if not number.isdigit():
            await ctx.send("Not a number")
        else:
            await self.bot.db.updatenumber(int(number), ctx.author.id, ctx.guild.id)
            await ctx.message.add_reaction("✅")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):

        if not self.bot.ready():
            return


        if not payload.guild_id:
            return
        if payload.channel_id != await self.bot.db.getcountingchannel(payload.guild_id):
            return

        message = payload.cached_message
        if not message: return
        if not message.content: return

        if message.content[0].isdigit():
            number = clean(message.content)
            last_number = await self.bot.db.getnumber(message.guild.id)
            if number == last_number:
                await message.channel.send(f"The last number was deleted. The next number is `{last_number+1}`")

    @commands.Cog.listener()
    async def on_raw_message_edit(self, payload):

        if not self.bot.ready():
            return

        if not payload.guild_id:
            return
        if payload.channel_id != await self.bot.db.getcountingchannel(payload.guild_id):
            return

        message = payload.cached_message
        if not message: return
        if not message.content: return

        if message.content[0].isdigit():
            number = clean(message.content)
            last_number = await self.bot.db.getnumber(message.guild.id)
            if number == last_number:
                await message.channel.send(f"The last number was edited. The next number is `{last_number+1}`")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if not self.bot.ready():
            return

        if not payload.guild_id:
            return
        if payload.channel_id != await self.bot.db.getcountingchannel(payload.guild_id):
            return
        if payload.user_id == self.bot.user.id:
            return
        if not payload.emoji.is_unicode_emoji():
            return
        if payload.emoji.name not in ["✅", "☑️", "✔️"]:
            return

        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        count = 0
        for reaction in message.reactions:
            if reaction.emoji in ["✅", "☑️", "✔️"]:
                count += reaction.count

        if count == 1:
            last_number = await self.bot.db.getnumber(payload.guild_id)
            await channel.send(f"A message was given a fake check. The next number is `{last_number+1}`")

async def setup(bot):
    await bot.add_cog(Counting(bot))