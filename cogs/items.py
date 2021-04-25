from discord.ext import commands
from functions import predicate
from random import choice
import economy as e

LARROW_EMOJI = "⬅️"
RARROW_EMOJI = "➡️"

def add(rewards, item, amount):
    if item in rewards:
        rewards[item] += amount
    else:
        rewards[item] = amount
    return rewards

class items(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="buy")
    async def _Buy(self, ctx, item, amount=1):
        await ctx.send("No items are purchaseable at the moment")

    @commands.command(name="sell")
    async def _Sell(self, ctx, item, amount="1"):
        item = item.lower()
        if item in e.items:
            if e.items[item][4] == "collectible":
                if amount.isdigit() or amount == "all":
                    user_id = ctx.author.id
                    owned = self.bot.db.getitem(user_id, item)
                    if amount.isdigit():
                        amount = int(amount)
                    else:
                        amount = owned
                    if amount <= owned:
                        value = (e.items[item][3] * amount) // 2
                        self.bot.db.updatebal(user_id, value)
                        value = self.bot.fn.fnum(value)
                        self.bot.db.removeitem(user_id, item, amount)
                        name = e.items[item][0]
                        await ctx.send(f"Sold **{amount} {name}(s)** for {value}, "
                                       f"you have **{owned - amount}** left")
                    elif owned:
                        await ctx.send("You don't have that many to sell!")
                    else:
                        await ctx.send("You don't any to sell!")
                else:
                    await ctx.send("That's not a a valid amount")
            else:
                await ctx.send("Only collectibles can be sold")
        else:
            await ctx.send("That item doesn't exist")

    @commands.command(name="use")
    async def _Use(self, ctx, item, amount="1"):
        item = item.lower()
        if item in e.items:
            if amount.isdigit() or amount == "all":
                user_id = ctx.author.id
                owned = self.bot.db.getitem(user_id, item)
                if amount.isdigit():
                    amount = int(amount)
                else:
                    amount = owned
                name = e.items[item][0]
                if amount <= owned and owned:
                    cat = e.items[item][4]
                    if cat == "collectible":
                        msg = (f"{name} is a collectible and so can't be used, "
                               "however you can sell it for half its value")
                    elif cat == "Spamable":
                        if str(ctx.channel.type) == "private": guild_id = -1
                        else: guild_id = ctx.guild.id
                        multi = e.items[item][3] * amount
                        if self.bot.ftime.isweekend(): multi *= 2
                        self.bot.db.increasemultiplier(user_id, guild_id, multi)
                        multi = f"`x{multi/10000}` multi (worth `{multi}` messages!)"
                        msg = (f"You spam **{amount} {name}(s)** and gain {multi}, "
                               f"you have **{owned - amount}** left")
                    elif cat == "Boost":
                        pass
                    elif cat == "Legendary Boost":
                        pass
                    elif cat == "Pet":
                        msg = ("You can't *use* a pet, "
                               "type `{prefix}pet` for help on pets")
                    elif cat == "FBox":
                        rewards = {}
                        for i in range(amount):
                            if item == "cfbox":
                                spamable = choice(e.spamables)
                                add(rewards, spamable, 5)
                            elif item == "ufbox":
                                spamable = choice(e.spamables)
                                collectible = choice(e.collectibles)
                                add(rewards, spamable, 10)
                                add(rewards, collectible, 1)
                            elif item == "rfbox":
                                spamable = choice(e.spamables)
                                collectible = choice(e.collectibles)
                                boost = choice(e.boosts)
                                add(rewards, spamable, 20)
                                add(rewards, collectible, 2)
                                add(rewards, boost, 1)
                            elif item == "lfbox":
                                spamable = choice(e.spamables)
                                collectible = choice(e.collectibles)
                                boost = choice(e.boosts)
                                legendary = choice(e.lboosts + e.pets)
                                add(rewards, spamable, 25)
                                add(rewards, collectible, 3)
                                add(rewards, boost, 2)
                                add(rewards, legendary, 1)
                        frewards = []
                        for reward in rewards:
                            self.bot.db.additem(user_id, reward, rewards[reward])
                            rname = e.items[reward][0]
                            frewards.append(f"**{rewards[reward]}x {rname}**")
                        frewards = ", ".join(frewards)
                        msg = (f"You opened **{amount} {name}(es)** and got "
                               + frewards +
                               f"! You have **{owned - amount} {name}(es)** left")
                    self.bot.db.removeitem(user_id, item, amount)
                    await ctx.send(msg)
                elif owned:
                    await ctx.send("You don't have that many to use!")
                else:
                    await ctx.send("You don't any to use!")
            else:
                await ctx.send("That's not a a valid amount")
        else:
            await ctx.send("That item doesn't exist")

    @commands.command(name="inv")
    async def _Inventory(self, ctx):
        fn = self.bot.fn
        inv = self.bot.db.getinventory(ctx.author.id)
        embeds = [fn.embed(ctx.author, f"{ctx.author.name}'s inventory", "")]
        count = 0
        for item in e.items:
            if item not in inv: continue
            if not inv[item]: continue
            if count and count % 6 == 0:
                embeds.append(fn.embed(ctx.author, f"{ctx.author.name}'s inventory"))
            data = e.items[item]
            embeds[-1].description += f"\n{data[2]} {data[0]} `{item}`\n"
            embeds[-1].description += f"Value: {fn.fnum(data[3])} Owned: **{inv[item]}**\n"
            count += 0
        if len(embeds[0].description.split("\n")) == 1:
            embeds[-1].description = "Looks like your inventory is empty!"

        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
            return

        page = 0
        embeds[page].set_footer(text=f"Page {page+1}/{len(embeds)}")
        msg = await ctx.send(embed=embeds[page])

        await msg.add_reaction(LARROW_EMOJI)
        await msg.add_reaction(RARROW_EMOJI)

        def check(reaction, user):
            emoji = (str(reaction.emoji) in [LARROW_EMOJI, RARROW_EMOJI])
            author = (user == ctx.author)
            message = (reaction.message.id == msg.id)
            return emoji and author and message

        wait = self.bot.wait_for
        async def forreaction():
            return await wait("reaction_add", timeout=60, check=check)

        while True:
            try:
                reaction, user = await forreaction()
                try: await msg.remove_reaction(reaction, user)
                except: pass
                if reaction.emoji == LARROW_EMOJI:
                    page -= 1
                    if page == -1:
                        page += len(embeds)
                elif reaction.emoji == RARROW_EMOJI:
                    page += 1
                    if page == len(embeds):
                        page -= len(embeds)
                embeds[page].set_footer(text=f"Page {page+1}/{len(embeds)}")
                await msg.edit(embed=embeds[page])
            except:
                embed = embeds[page]
                embed.set_footer(text="Inventory timed out")
                try: await msg.edit(embed=embed)
                except: pass
                break

    @commands.command(name="store")
    async def _Store(self, ctx):
        fn = self.bot.fn
        embeds = [fn.embed(ctx.author, "The store",
                 "No are items are purchaseable from the store yet",
                 "You can use `fbot item <item>` for more info on an item\n")]
        count = 0
        for item in e.items:
            if count and count % 6 == 0:
                embeds.append(fn.embed(ctx.author, "The store",
                    "No are items are purchaseable from the store yet",
                    "You can use `fbot item <item>` for more info on an item\n"))
            data = e.items[item]
            embeds[-1].description += f"\n{data[2]} {data[0]} `{item}`\n"
            embeds[-1].description += f"**{data[4]}** - Value: {fn.fnum(data[3])}\n"
            count += 1

        page = 0
        embeds[page].set_footer(text=f"Page {page+1}/{len(embeds)}")
        msg = await ctx.send(embed=embeds[page])

        await msg.add_reaction(LARROW_EMOJI)
        await msg.add_reaction(RARROW_EMOJI)

        def check(reaction, user):
            emoji = (str(reaction.emoji) in [LARROW_EMOJI, RARROW_EMOJI])
            author = (user == ctx.author)
            message = (reaction.message.id == msg.id)
            return emoji and author and message

        wait = self.bot.wait_for
        async def forreaction():
            return await wait("reaction_add", timeout=60, check=check)

        while True:
            try:
                reaction, user = await forreaction()
                try: await msg.remove_reaction(reaction, user)
                except: pass
                if reaction.emoji == LARROW_EMOJI:
                    page -= 1
                    if page == -1:
                        page += len(embeds)
                elif reaction.emoji == RARROW_EMOJI:
                    page += 1
                    if page == len(embeds):
                        page -= len(embeds)
                embeds[page].set_footer(text=f"Page {page+1}/{len(embeds)}")
                await msg.edit(embed=embeds[page])
            except:
                embed = embeds[page]
                embed.set_footer(text="Store timed out")
                try: await msg.edit(embed=embed)
                except: pass
                break

    @commands.command(name="item")
    async def _Item(self, ctx, item):
        item = item.lower()
        if item in e.items:
            fn = self.bot.fn
            data = e.items[item]
            owned = self.bot.db.getitem(ctx.author.id, item)
            embed = fn.embed(ctx.author,
                    f"{data[2]} **{data[0]}** (`{item}`)", f"*{data[5]}*\n")
            embed.add_field(name="Owned", value=owned)
            embed.add_field(name="Value", value=fn.fnum(data[3], bold=False))
            embed.add_field(name="Usage",
                            value=f"This item {data[6]}", inline=True)
            embed.set_author(name=f"{data[4]}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("That item doesn't exist")

def setup(bot):
    bot.add_cog(items(bot))