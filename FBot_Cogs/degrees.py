from discord.ext import commands
from functions import predicate
from dbfn import reactionbook
import economy as e
import discord
import random
import time

f = "~~f~~ "

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="study")
    @commands.check(predicate)
    async def _Study(self, ctx):
        fn, db = self.bot.fn, self.bot.db
        user = ctx.author

        c = db.conn.cursor()
        t = (user.id,)
        c.execute("SELECT laststudy FROM users WHERE user_id=?", t)
        laststudy = c.fetchone()[0]
        if not laststudy <= time.time() / 60:
            wait = round(laststudy - time.time() / 60)
            await ctx.send(f"You must wait another {wait} mins to study again")
            return

        degree = db.getdegree(user.id)
        if degree == "None":
            await ctx.send("You're not taking a degree right now")
            return
        job = db.getjob(user.id)

        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)

        salary = e.salaries[e.degreejobs[degree]] * jobmulti
        if str(ctx.channel.type) == "private":
            salary *= db.getusermulti(user.id)
        else:
            multis = db.getmultis(user.id, ctx.guild.id)
            salary *= multis[0] * multis[1]

        debt = round(salary * random.uniform(0.1, 0.5))

        progress, newdebt = db.study(user.id, debt)
        length = e.courses[degree][0]
        if progress == length:
            db.finishdegree(user.id)
            db.startjob(user.id, e.degreejobs[degree])
            end = f"You may now apply for the **{e.degreejobs[degree]}** job"
        else:
            db.studied(user.id)
            end = f"Degree course progress: `{progress}/{length}`"
        embed = fn.embed(user, f"You studied for **{degree}**",
                f"You studied and gained {fn.fnum(debt)} debt",
                f"You now have {fn.fnum(newdebt)} debt", end)
        await ctx.send(embed=embed)
        if debt == newdebt: return

        bal, debt = db.getbal(user.id)
        if not bal:
            db.updatedebt(user.id, salary)
            msg = ("They laugh at your empty balance\n" +
                   f"You gain {fn.fnum(salary)} more debt")
        elif debt > bal:
            debt = salary * random.uniform(0.1, 0.5)
            salary = salary * random.uniform(0.1, 0.5)
            db.updatedebt(user.id, debt)
            db.setbal(user.id, bal - salary)
            msg = ("They laugh at your overwhelming debt\n" +
                   f"You gain {fn.fnum(debt)} more debt\n" +
                   f"While loosing {fn.fnum(salary)}")
        else:
            if not debt: return
            if random.randint(0, 1): return
            salary = salary * random.uniform(0.1, 0.5)
            db.setbal(user.id, bal - salary)
            msg = ("They pinch some of your fbux\n" +
                   f"You loose {fn.fnum(salary)}")
        embed = fn.embed(user, "You get a visit from the debt collectors!",
                         msg)
        await ctx.send(embed=embed)

    @commands.command(name="degrees")
    @commands.check(predicate)
    async def _Degrees(self, ctx):
        db = self.bot.db

        book = reactionbook(self.bot, ctx)
        for tier in e.degrees:
            tierdegrees = {}
            for degree, length, multi in e.degrees[tier]:
                out = "**"
                if degree == db.getdegree(ctx.author.id):
                    reqs = "📝"
                elif e.degreejobs[degree] in db.getjobs(ctx.author.id):
                    reqs = "✅"
                elif db.getusermulti(ctx.author.id) >= multi:
                    reqs = "🔓"
                else:
                    reqs, out = "🔒", "~~"
                job = e.degreejobs[degree]
                tierdegrees[degree] = (job, length, multi, reqs, out)
            book.createpages(tierdegrees,
                             LINE="%3 %4__%l__ - *unlocks %0*%4\n"
                             "Course length: `%1`, Requires `x%2` multiplier\n",
                             SUBHEADER=f"**FBot Degrees - Tier {tier}**\n")
        await book.createbook(COLOUR=self.bot.db.getcolour(ctx.author.id))

    @commands.command(name="degree")
    @commands.check(predicate)
    async def _Degree(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum
        degree = db.getdegree(user.id)
        title = f"{user.display_name}'s degree information"
        if degree == "None":
            embed = self.bot.fn.embed(user, title,
                    "Not currently taking a degree")
        else:
            if db.getjob(user.id) == "Unemployed": jobmulti = 1.0
            else: jobmulti = db.getjobmulti(user.id)
            job = e.degreejobs[degree]
            salary = e.salaries[e.degreejobs[degree]] * jobmulti
            if str(ctx.channel.type) == "private":
                salary *= db.getusermulti(user.id)
            else:
                multis = db.getmultis(user.id, ctx.guild.id)
                salary *= multis[0] * multis[1]
            progress = db.progress(user.id)
            length = e.courses[degree][0]
            debtl, debtu = salary * 0.1, salary * 0.5
            embed = self.bot.fn.embed(user, title,
                    f"Currently taking **{degree}** for **{job}**",
                    f"Progress: **{progress}/{length}**",
                    f"Debt range: {fnum(debtl)} - {fnum(debtu)}")
        await ctx.send(embed=embed)

    @commands.command(name="take")
    @commands.check(predicate)
    async def _Take(self, ctx, *, degree):
        degree = degree.lower()
        if degree in e.degreenames:
            db = self.bot.db
            user = ctx.author
            degree = e.degreenames[degree]
            if db.getusermulti(user.id) >= e.courses[degree][1]:
                if e.degreejobs[degree] not in db.getjobs(user.id):
                    if db.getdegree(user.id) == "None":
                        db.changedegree(user.id, degree)
                        db.studied(user.id)
                        embed = self.bot.fn.embed(user,
                                f"You are now taking the degree: `{degree}`",
                                "Please wait an hour before you start studying")
                        embed.set_author(name="Application accepted!")
                        await ctx.send(embed=embed)
                        return
                    else: message = "You are currently taking a degree"
                else: message = "You have already completed this degree"
            else: message = "You do not meet the requirements to take this degree"
        else: message = "This degree does not exist, how odd"
        await ctx.send(message)

    @commands.command(name="drop")
    @commands.check(predicate)
    async def _Drop(self, ctx):
        db = self.bot.db
        degree = db.getdegree(ctx.author.id)
        if degree != "None":
            db.drop(ctx.author.id)
            message = f"You have dropped **{degree}**\nYou may take it again at anytime"
        else:
            message = "You have can't drop your degree, you're not taking one!"
        await ctx.send(message)

def setup(bot):
    bot.add_cog(economy(bot))