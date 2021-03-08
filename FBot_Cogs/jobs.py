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

    @commands.command(name="work")
    @commands.check(predicate)
    async def _Work(self, ctx):
        user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum

        c = db.conn.cursor()
        t = (user.id,)
        c.execute("SELECT lastwork FROM users WHERE user_id=?", t)
        lastwork = c.fetchone()[0]
        if not lastwork <= time.time() / 60:
            wait = round(lastwork - time.time() / 60)
            await ctx.send(f"You must wait another {wait} mins to work again")
            return

        job = db.getjob(user.id)
        tax = random.uniform(0.1, 0.5) * 100

        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)

        salary = e.salaries[job] * jobmulti
        if str(ctx.channel.type) == "private":
            salary *= db.getusermulti(user.id)
        else:
            multis = db.getmultis(user.id, ctx.guild.id)
            salary *= multis[0] * multis[1]

        income = round(salary * (tax / 100))
        balance = db.work(user.id, job, income)
        embed = self.bot.fn.embed(user, "FBot work",
                f"You work and earn: **{fnum(salary)}**",
                f"After {100 - round(tax)}% tax deductions: {fnum(income)}",
                f"Your new balance is: {fnum(balance)}")
        await ctx.send(embed=embed)

        bal, debt = db.getbal(user.id)
        degree = db.getdegree(user.id)
        if degree != "None":
            salary = e.salaries[e.degreejobs[degree]]
        else:
            salary = e.salaries[job]
        salary *= db.getusermulti(user.id) * jobmulti
        if not bal:
            db.updatedebt(user.id, salary)
            msg = ("They laugh at your empty balance\n" +
                   f"You gain {fnum(salary)} more debt")
        elif debt > bal:
            debt = salary * random.uniform(0.1, 0.5)
            salary = salary * random.uniform(0.1, 0.5)
            db.updatedebt(user.id, debt)
            db.setbal(user.id, bal - salary)
            msg = ("They laugh at your overwhelming debt\n" +
                   f"You gain {fnum(debt)} more debt\n" +
                   f"While loosing {fnum(salary)}")
        else:
            if not debt: return
            if random.randint(0, 1): return
            salary = salary * random.uniform(0.1, 0.5)
            db.setbal(user.id, bal - salary)
            msg = ("They pinch some of your fbux\n" +
                   f"You loose {fnum(salary)}")
        embed = self.bot.fn.embed(user, "You get a visit from the debt collectors!",
                         msg)
        await ctx.send(embed=embed)

    @commands.command(name="jobs")
    @commands.check(predicate)
    async def _Jobs(self, ctx):
        db = self.bot.db

        book = reactionbook(self.bot, ctx)
        for tier in e.jobs:
            if not tier: continue
            tierjobs = {}
            for job, salary, desc in e.jobs[tier]:
                out = "**"
                if db.getjob(ctx.author.id) == job:
                    quals = "📝"
                elif job in db.getjobs(ctx.author.id):
                    quals = "🔓"
                else:
                    quals, out = "🔒", "~~"
                degree = e.jobdegrees[job]
                tierjobs[job] = (degree, self.bot.fn.fnum(salary),
                                 desc, quals, out)
            book.createpages(tierjobs,
                             LINE="%3 %4__%l__ - *needs %0*%4\n"
                             "Salary: %1\n*%2*\n",
                             SUBHEADER=f"**FBot Jobs - Tier {tier}**\n")
        await book.createbook(COLOUR=self.bot.db.getcolour(ctx.author.id))

    @commands.command(name="job")
    @commands.check(predicate)
    async def _Job(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum
        job = db.getjob(user.id)
        title = f"{user.display_name}'s job information"
        salary = e.salaries[job]

        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)

        salary = e.salaries[job] * jobmulti
        if str(ctx.channel.type) == "private":
            salary *= db.getusermulti(user.id)
        else:
            multis = db.getmultis(user.id, ctx.guild.id)
            salary *= multis[0] * multis[1]
        incomel, incomeu = salary * 0.1, salary * 0.5
        embed = self.bot.fn.embed(user, title,
                f"Currently taking **{job}**",
                f"Salary: {fnum(salary)}",
                f"After tax: {fnum(incomel)} - {fnum(incomeu)}")
        await ctx.send(embed=embed)

    @commands.command(name="apply")
    @commands.check(predicate)
    async def _Apply(self, ctx, *, job):
        job = job.lower()
        if job == "unemployed":
            message = "You can't apply to be unemployed, just `FBot resign`"
        elif job in e.jobnames:
            db = self.bot.db
            user = ctx.author
            job = e.jobnames[job]
            if job in db.getjobs(user.id):
                if db.getjob(user.id) == "Unemployed":
                    db.changejob(user.id, job)
                    db.worked(user.id)
                    embed = self.bot.fn.embed(user,
                            f"You have been given the job: `{job}`",
                            "Please wait an hour before you start working")
                    embed.set_author(name="Application accepted!")
                    await ctx.send(embed=embed)
                    return
                else: message = "You must resign first"
            else: message = "You are not qualified for this job"
        else: message = "This job does not exist, how odd"
        await ctx.send(message)

    @commands.command(name="resign")
    @commands.check(predicate)
    async def _Resign(self, ctx):
        db = self.bot.db
        job = db.getjob(ctx.author.id)
        if job != "Unemployed":
            db.resign(ctx.author.id)
            an = "an" if job[0].lower() in "aeiou" else "a"
            if job.startswith("FB"): an = "an"
            message = f"You have resigned as {an} **{job}**\nYou may re-apply at anytime"
        else:
            message = "You have can't resign, you're unemployed!"
        await ctx.send(message)

def setup(bot):
    bot.add_cog(economy(bot))