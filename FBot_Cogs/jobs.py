from discord.ext import commands
from functions import cooldown
from datetime import datetime
import economy as e
import discord
import sqlite3
import random
import dbfn

f = "~~f~~ "

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="work")
    @commands.check(cooldown)
    async def _Work(self, ctx):
        user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum

        c = db.conn.cursor()
        t = (user.id,)
        c.execute("SELECT lastwork FROM users WHERE user_id=?", t)
        lastwork = c.fetchone()[0]
        if not lastwork <= datetime.now().timestamp() / 60:
            wait = round(lastwork - datetime.now().timestamp() / 60)
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

        # Chance of debt collectors

    @commands.command(name="jobs")
    @commands.check(cooldown)
    async def _Jobs(self, ctx):
        db = self.bot.db

        book = dbfn.reactionbook(self.bot, ctx)
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
                             LINE=f"%3 %4__%l__ - *needs %0*%4\n"
                             f"Salary: %1\n*%2*\n",
                             SUBHEADER=f"**FBot Jobs - Tier {tier}**\n")
        await book.createbook(COLOUR=self.bot.db.getcolour(ctx.author.id))

    @commands.command(name="job")
    @commands.check(cooldown)
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
        embed = self.bot.fn.embed(ctx.author, title,
                f"Currently taking **{job}** ({fnum(salary)})",
                f"After tax: {fnum(incomel)} - {fnum(incomeu)}")
        await ctx.send(embed=embed)

    @commands.command(name="apply")
    @commands.check(cooldown)
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
    @commands.check(cooldown)
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
