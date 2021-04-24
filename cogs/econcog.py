﻿from discord.ext import commands
from functions import predicate
import economy as e
import discord

LARROW_EMOJI = "⬅️"
RARROW_EMOJI = "➡️"
toptypes = ["votes", "counting", "multi", "servmulti",
            "bal", "netbal", "fbux", "netfbux", "debt", "netdebt"]

class fakeuser: id = 0
user = fakeuser()

def formatname(name, ID):
    if not name:
        name = "Deleted User"
    else:
        name = name.name.replace("*", "")
        name = name.replace("`", "")
        name = name.replace("_", "")
        name = name.replace("||", "")
        #name = f"<@!{ID}> ({name})"
    return name

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    @commands.check(predicate)
    async def _Profile(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum
        profile = list(db.getprofile(user.id))
        job = profile[4]
        if profile[5] == "None":
            degree = "No degree"
        else:
            degree = profile[5]
            degree = f"{degree} - {profile[6]}/{e.courses[degree][0]}"
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s profile:")
        embed.add_field(name="FBux", value=fnum(profile[0]))
        embed.add_field(name="Debt", value=fnum(profile[2]))
        embed.add_field(name="Job", value=job)
        embed.add_field(name="Net FBux", value=fnum(profile[1]))
        embed.add_field(name="Net Debt", value=fnum(profile[3]))
        embed.add_field(name="Degree", value=degree)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="gift")
    @commands.is_owner()
    @commands.check(predicate)
    async def _Gift(self, ctx, amount, user: discord.User=None):
        if not user: user = ctx.author
        self.bot.db.updatebal(user.id, amount)
        await ctx.send("Lucky you")

    @commands.command(name="payoff")
    @commands.check(predicate)
    async def _PayOff(self, ctx, amount):
        fn, db = self.bot.fn, self.bot.db
        bal, debt = db.getbal(ctx.author.id)
        if amount == "all":
            amount = debt
        elif amount.isdigit():
            amount = int(amount)
        else:
            await ctx.send("That's not a valid amount")
            return
        if not debt:
            await ctx.send("You don't have any debt to pay off!")
        elif amount > debt:
            await ctx.send("You don't have that much debt to pay off!")
        else:
            if db.getjob(ctx.author.id) == "Unemployed": jobmulti = 1.0
            else: jobmulti = db.getjobmulti(ctx.author.id)
            interest = round(db.getusermulti(ctx.author.id) * jobmulti, 4)
            loss = round(amount * interest)
            if loss > bal:
                embed = fn.embed(user, "You try and pay off debt",
                    f"The debt you owe accumulates `{interest}%` interest",
                    f"Your measly balance, {fn.fnum(bal)}",
                    f"Can't afford to pay {fn.fnum(loss)} worth of debt")
            else:
                db.payoff(ctx.author.id, amount, loss)
                embed = fn.embed(user, "You try and pay off debt",
                    f"The debt you owe accumulates `{interest}%` interest",
                    f"Your loose {fn.fnum(loss)}",
                    f"But pay off {fn.fnum(amount)} worth of debt")
            await ctx.send(embed=embed)

    @commands.command(name="bal")
    @commands.check(predicate)
    async def _Balance(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum
        bal, debt = db.getbal(user.id)
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s balance",
                f"FBux: {fnum(bal)}", f"Debt: {fnum(debt)}")
        await ctx.send(embed=embed)

    @commands.command(name="multis")
    @commands.check(predicate)
    async def _Multipliers(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        job = db.getjob(user.id)
        if job == "Unemployed":
            jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)
        if str(ctx.channel.type) == "private":
            multi = db.getusermulti(user.id)
            message = f"Personal Multiplier: `x{multi}`"
        else:
            multis = db.getmultis(user.id, ctx.guild.id)
            message = (f"Personal Multiplier: `x{multis[0]}`\n"
                       f"Server Multiplier: `x{multis[1]}`")
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s multipliers:",
                message + f"\n{job} Multiplier: `x{jobmulti}`")
        await ctx.send(embed=embed)

    @commands.command(name="top")
    @commands.check(predicate)
    async def _Top(self, ctx, toptype):

        toptype = toptype.lower().replace("multis", "multi")
        if toptype in toptypes:
            if toptype in ["counting", "servmulti"]:
                if str(ctx.channel.type) == "private":
                    await ctx.send(f"Top {toptype} can only be used in a server")
                    return
                obj_id = ctx.guild.id
            else:
                obj_id = ctx.author.id

            async with ctx.channel.typing():
                fn, db = self.bot.fn, self.bot.db
                top, selftop, rank = db.gettop(toptype, 12, obj_id)
                if toptype == "vote":
                    selftop = f"with `{selftop}` vote(s) this month"
                elif toptype == "counting":
                    selftop = f"with a highscore of `{selftop}`"
                elif toptype == "multi":
                    selftop = f"with a multiplier of `x{selftop/10000}`"
                elif toptype == "servmulti":
                    selftop = f"with a server multiplier of `x{selftop/1000000}`"
                else:
                    selftop = f"with {fn.fnum(selftop)}"
                embed = fn.embed(ctx.author, f"FBot Top {toptype}",
                                 f"Ranked `{rank}` " + selftop)

                cache = self.bot.cache["Names"]
                for rank, row in enumerate(top):
                    ID, typeitem = row
                    name = cache.get(ID)
                    if not name:
                        if toptype in ["counting", "servmulti"]:
                            try: name = self.bot.get_guild(ID).name
                            except: name = "Unknown Server"
                            if ctx.guild.id == ID:
                                name = f"**--> __{name}__ <--**"
                        else:
                            name = formatname(await self.bot.fetch_user(ID), ID)
                            if ctx.author.id == ID:
                                name = f"**--> __{name}__ <--**"
                        cache.add(ID, name)

                    rank = str(rank + 1)
                    if rank == "1": medal = ":first_place:"
                    elif rank == "2": medal = ":second_place:"
                    elif rank =="3": medal = ":third_place:"
                    else: medal = ":medal:"

                    if rank.endswith("1") and rank != "11": rank = f"{medal} {rank}st with "
                    elif rank.endswith("2") and rank != "12": rank = f"{medal} {rank}nd with "
                    elif rank.endswith("3") and rank != "13": rank = f"{medal} {rank}rd with "
                    else: rank = f"{medal} {rank}th with "

                    if toptype == "votes": content = f"{typeitem} votes"
                    elif toptype == "counting": content = f"`{typeitem}`"
                    elif toptype == "multi": content = f"`x{typeitem/10000}`"
                    elif toptype == "servmulti": content = f"`x{typeitem/1000000}`"
                    else: content = fn.fnum(typeitem)
                    embed.add_field(name=rank + content, value=name)

            await ctx.send(embed=embed)

        else:
            await ctx.send("We don't have a leaderboard for that...")

def setup(bot):
    bot.add_cog(economy(bot))