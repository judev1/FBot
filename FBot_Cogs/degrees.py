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

    @commands.command(name="study")
    @commands.check(cooldown)
    async def _Study(self, ctx):
        db = self.bot.db
        user = ctx.author

        c = db.conn.cursor()
        t = (user.id,)
        c.execute("SELECT laststudy FROM users WHERE user_id=?", t)
        laststudy = c.fetchone()[0]
        if not laststudy <= datetime.now().timestamp() / 60:
            wait = round(laststudy - datetime.now().timestamp() / 60)
            await ctx.send(f"You must wait another {wait} mins to study again")
            return

        degree = db.getdegree(user.id)
        if degree == "None":
            await ctx.send("You're not taking a degree right now")
            return
        salary = e.salaries[db.getjob(user.id)]
        debt = round(salary * random.uniform(0.05, 0.40))
        
        progress, newdebt = db.study(user.id, debt)
        length = e.courses[degree][0]
        if progress == length:
            db.finishdegree(user.id)
            db.startjob(user.id, e.degreejobs[degree])
            embed = self.bot.fn.embed(user, "Degree completed!",
                    f"You studied and gained debt: **{f}{round(debt)}**",
                    f"Your new debt is: **{f}{newdebt}**",
                    f"You may now apply for the **{e.degreejobs[degree]}** job")
        else:
            db.studied(user.id)
            embed = self.bot.fn.embed(user, f"You studied for **{degree}**",
                    f"You studied and gained debt: **{f}{debt}**",
                    f"Your new debt is: **{f}{newdebt}**",
                    f"Degree course progress: `{progress}/{length}`")
        await ctx.send(embed=embed)
        # Chance of debt collectors            

    @commands.command(name="degrees")
    @commands.check(cooldown)
    async def _Degrees(self, ctx):
        db = self.bot.db

        book = dbfn.reactionbook(self.bot, ctx)
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
                             LINE=f"%3 %4__%l__ - *unlocks %0*%4\n"
                             "Course length: `%1`, Requires `x%2` multiplier\n",
                             SUBHEADER=f"**FBot Degrees - Tier {tier}**\n")
        await book.createbook(COLOUR=self.bot.db.getcolour(ctx.author.id))

    @commands.command(name="degree")
    @commands.check(cooldown)
    async def _Degree(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        degree = db.getdegree(user.id)
        title = f"{user.display_name}'s degree information"
        if degree == "None":
            embed = self.bot.fn.embed(user, title,
                    "Not currently taking a degree")
        else:
            progress = db.progress(user.id)
            length = e.courses[degree][0]
            job = e.degreejobs[degree]
            salary = e.salaries[job]
            debtl = round(salary * 0.05)
            debtu = round(salary * 0.40)
            embed = self.bot.fn.embed(ctx.author, title,
                    f"Currently taking **{degree}** for **{job}**",
                    f"Progress: **{progress}/{length}**",
                    f"Debt range: **{f}{debtl}** - **{f}{debtu}**")
        await ctx.send(embed=embed)

    @commands.command(name="take")
    @commands.check(cooldown)
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
    @commands.check(cooldown)
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
