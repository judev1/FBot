from discord.ext.commands import MemberConverter
from discord.ext import commands
from triggers import tr
import dbfn
import sqlite3
import random
import discord

f = "~~f~~ "
# TIER ONE
t1jobs = {"Unemployed": [1000, "You gotta dismantle the government somehow"], # No degree, starting job
          "Waitor": [8000, "This seems like a good idea you said, I'll enjoy this a lot you said"],
          "Janitor": [10000, "They ask you how you are, and you just have to say you're fine when you're not really fine, but you just can't get into it, because they would never understand"],
          "Plumber": [15000, "Just because you're not a janitor doesn't mean I'll let you near my kids"]
          }
t1degrees = {"Food Touching": [1, 1, "Waitor"],
             "Touching": [3, 1.01, "Janitor"],
             "Touching Shit": [5, 1.05, "Plumber"]
             }
# TIER TWO
t2jobs = {"Loan Shark": [20000, "No one can escape debt, **no one**"],
         "Physic": [25000, "I only work 9 to 5, except between 10 to 3 when I'm having lunch, and I'm available all weekdays, except for Monday, Wednesday, Thursday and Friday, that'll be 25000 for the first session and you'll need to pay for the next 8 seesions, with intrest of course. So when can I expect to see you?"]
          }
t2degrees = {"Baiting": [8, 1.1, "Loan Shark"],
             "Bullshittery": [14, 1.15, "Physic"]
             }
# TIER THREE
t3jobs = {}
t3degrees = {}
# TIER FOUR
t4jobs = {}
t4degrees = {}
# TIER FIVE
t5jobs = {}
t5degrees = {}
# TIER SIX
t6jobs = {"Resposible Inheriter": [50000000, "Your job is to recieve money from your rich and dying relatives"], # No degree
          "Irresposible Inheriter": [100000000, "Similar to resposible inheriter but with the mindset: Budget funerals are the way to go!"] # Becomes responsible
          }
t6degrees = {"Funding Trust": [60, 5, "Iresposible Inheriter"]
             }
# TIER SEVEN
t7jobs = {"Crime Lord": [200000000, "Even crime lords need a degree in crime lording"]
          }
t7degrees = {"Crime Lording": [80, 6, "Crime Lord"]
             }
# TIER EIGHT
t8jobs = {"Billionare": [1000000000, "The description is in the job title"],
          "FBot Deveolper": [0, "a c c u r a t e"], # Can't gain any debt # Gets a nice golden colour on their embeds, also FBot addresses them as Lord
          }
t8degrees = {"Becoming Rich Quik": [100, 8, "Billionare"],
             "clicky-clacky keyboard pressing": [150, 10, "FBot Dev"]
             }
# PUNNISHMENT JOBS
pjobs = {
         "Mormon": [-1000, "You devote your life to a good cause, for now at least"], # There is a chace you'll become enlightened whenever you switch jobs
         "Karen": [-5000, "Just great, now everyone hates you"], # When you have no debt and a lot of money (in tier 3)
         "Light Mode Enthusiast": [-50000, "Maybe if you stopped using discord light mode you might actually make some money"], # Not sure yet
         "Ex-FBot Deveolper": [-100000, "FBot has maintence costs, glad you noticed"] # When you change jobs after being an FBot Developer
         }

jobs = [t1jobs, t2jobs, t3jobs, t4jobs, t5jobs, t6jobs, t7jobs, t8jobs]
degrees = [t1degrees, t2degrees, t3degrees, t4degrees, t5degrees, t6degrees, t7degrees, t8degrees]

jobnames, degreenames = {}, {}
for tier in jobs:
    for job in tier:
        jobnames[job] = tier[job]
for tier in degrees:
    for degree in tier:
        degreenames[degree] = tier[degree]

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        fn, db = bot.fn, bot.db

        @self.bot.event
        async def _Multiply(message):
            # TODO: Check if FBot can talk in channel
            # TODO: Check if user is a bot
            user = message.author
            if str(message.channel.type) == "private": guild_id = 0
            else: guild_id = message.guild.id
            commandcheck = message.content[len(fn.getprefix(self.bot, message)):]
            for command in self.bot.walk_commands():
                if commandcheck.startswith(command.name):
                    db.increasemultiplier(user.id, guild_id, 2)
                    return
                for alias in command.aliases:
                    if commandcheck.startswith(alias):
                        db.increasemultiplier(user.id, guild_id, 2)
                        return
            priority, status = "all", "on"
            if str(message.channel.type) != "private":
                db.Add_Channel(message.channel.id, guild_id)
                priority = db.Get_Priority(guild_id)
                status = db.Get_Status(message.channel.id)
            if status == "on":
                trigger_detected = tr.trigger_respond(message, priority)[0]
                if trigger_detected:
                    db.increasemultiplier(user.id, guild_id, 1)
        self.bot.add_listener(_Multiply, "on_message")

    @commands.command(name="profile")
    async def _Profile(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        profile = list(db.getprofile(user.id))
        if profile[4] == "None": # WHEN NONE IS NO MORE DELETE
            job = f"Unemployed: {f}1000"
        else:
            job = f"{job}: {f}{jobs[job][0]}"
        if profile[5] == "None":
            degree = "No degree"
        else: degree = f"{profile[5]} - {profile[6]}/{degreenames[profile[5]][0]}"
        embed = self.bot.fn.embed(f"{user.display_name}'s profile:", "")
        embed.add_field(name="FBux", value=profile[0])
        embed.add_field(name="Debt", value=profile[2])
        embed.add_field(name="Job", value=job)
        embed.add_field(name="Net FBux", value=profile[1])
        embed.add_field(name="Net Debt", value=profile[3])
        embed.add_field(name="Degree", value=degree)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="jobs")
    async def _Jobs(self, ctx):
        db = self.bot.db

        i = 1
        book = dbfn.reactionbook(self.bot, ctx)
        for tier in jobs.copy():
            for job in tier:
                
                # WHEN NONE IS NO MORE DELETE
                if job == "Unemployed": job = "None"
                
                if db.getjob(ctx.author.id) in [job]:
                    quals = ["📝"]
                elif job in db.getjobs(ctx.author.id):
                    quals = ["🔓"]
                else:
                    quals = ["🔒"]

                # WHEN NONE IS NO MORE DELETE
                if job == "None": job = "Unemployed"

                tier[job] += quals
            book.createpages(tier, LINE=f"%2 **%l** - {f}%0\n*%1*\n",
                             SUBHEADER=f"**FBot Jobs - Tier {i}**\n")
            i += 1
        await book.createbook(COLOUR=self.bot.fn.red)

    @commands.command(name="degrees")
    async def _Degrees(self, ctx):
        db = self.bot.db

        i = 1
        book = dbfn.reactionbook(self.bot, ctx)
        for tier in degrees.copy():
            for degree in tier:
                if degree == db.getdegree(ctx.author.id):
                    reqs = ["📝"] 
                elif tier[degree][2] in db.getjobs(ctx.author.id):
                    reqs = ["✅"]
                elif round(db.getusermulti(ctx.author.id) / 10**4, 2) >= tier[degree][1]:
                    reqs = ["🔓"]
                else:
                    reqs = ["🔒"]
                tier[degree] += reqs
            book.createpages(tier, LINE=f"%3 **%l**\n"
                             "Course length: `%0`, Requires `x%1` multiplier\n",
                             SUBHEADER=f"**FBot Degrees - Tier {i}**\n")
            i += 1
        await book.createbook(COLOUR=self.bot.fn.red)

    @commands.command(name="apply")
    async def _Apply(self, ctx, *, job):
        if job in jobnames:
            db = self.bot.db
            user = ctx.author
            if job in db.getjobs(user.id):
                if db.getjob(user.id) == "None": # UNEMPLOYED
                    db.changejob(user.id, job)
                    db.worked(user.id)
                    embed = self.bot.fn.embed("You have been given the job: `{job}`",
                               "Please wait an hour before you start working")
                    embed.set_author(name="Application accepted!")
                    await ctx.send(embed=embed)
                    return
                else: message = "You must resign first"
            else: message = "You are not qualified for this job"
        else: message = "This job does not exist, how odd"
        await ctx.send(message)

    @commands.command(name="take")
    async def _Take(self, ctx, *, degree):
        if degree in degreenames:
            db = self.bot.db
            user = ctx.author
            if round(db.getusermulti(user.id) / 10**4, 2) >= degreenames[degree][1]:
                if degreenames[degree][2] not in db.getjobs(user.id):
                    if db.getdegree(user.id) == "None":
                        db.changedegree(user.id, degree)
                        db.studied(user.id)
                        embed = self.bot.fn.embed(f"You are now taking the degree: `{degree}`",
                                   "Please wait an hour before you start studying")
                        embed.set_author(name="Application accepted!")
                        await ctx.send(embed=embed)
                        return
                    else: message = "You are currently taking a degree"
                else: message = "You have already completed this degree"
            else: message = "You do not meet the requirements to take this degree"
        else: message = "This degree does not exist, how odd"
        await ctx.send(message)
    
    @commands.command(name="work")
    @commands.cooldown(1, 3600, type=commands.BucketType.user)
    async def _Work(self, ctx):
        db = self.bot.db
        user = ctx.author
        if db.canwork(user.id):
            # guild value for private channels
            job = db.getjob(user.id)
            multis = db.getmultis(user.id, ctx.guild.id)
            
            # WHEN NONE IS NO MORE DELETE
            if job == "None": job = "Unemployed"
            
            salary = round(jobnames[job][0] * multis[0] * multis[1])
            tax = random.uniform(0.1, 0.5) * 100
            income = round(salary * (tax / 100))
            balance = db.work(user.id, job, income)
            embed = self.bot.fn.embed("FBot work",
                    f"You work and earn: **{f}{salary}**\n"
                    f"After {100 - round(tax)}% tax deductions: **{f}{income}**\n"
                    f"Your new balance is: **{f}{balance}**")
            await ctx.send(embed=embed)
        else:
            wait = db.lastwork(user.id)
            await ctx.send(f"You must wait another {wait} mins to work again")

    @_Work.error
    async def on_command_error(self, ctx, error):
        if type(error) is commands.CommandOnCooldown:
            wait = self.bot.db.lastwork(ctx.author.id)
            await ctx.send(f"You must wait another {wait} mins to work again")

    @commands.command(name="study")
    @commands.cooldown(1, 3600, type=commands.BucketType.user)
    async def _Study(self, ctx):
        db = self.bot.db
        user = ctx.author
        if db.canstudy(user.id):
            # guild value for private channels
            degree = db.getdegree(user.id)
            if degree == "None":
                await ctx.send("You're not taking a degree right now")
                return
            progress = db.study(user.id)
            length = degreenames[degree][0]
            if progress == length:
                db.finishdegree(user.id)
                db.startjob(user.id, degreenames[degree][2])
                embed = self.bot.fn.embed("Degree completed!",
                        f"You may now apply for the **{degreenames[degree][2]} job**")
            else:
                self.bot.db.studied(user.id)
                embed = self.bot.fn.embed(f"You studied for **{degree}**",
                        f"Degree course progress: `{progress}/{length}`")
            await ctx.send(embed=embed)
        else:
            wait = self.bot.db.laststudy(user.id)
            await ctx.send(f"You must wait another {wait} mins to study again")

    @_Study.error
    async def on_command_error(self, ctx, error):
        print(error)
        if type(error) is commands.CommandOnCooldown:
            wait = self.bot.db.laststudy(ctx.author.id)
            await ctx.send(f"You must wait another {wait} mins to study again")

    @commands.command(name="balance", aliases=["bal"])
    async def _Balance(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        balance = db.getbal(user.id)
        embed = self.bot.fn.embed(f"{user.display_name}'s balance: "
                                  f"{f}{balance}", "")
        await ctx.send(embed=embed)

    @commands.command(name="multis", aliases=["multipliers"])
    async def _Multipliers(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        job = db.getjob(user.id)
        # CHANGE TO UNEMPLOYED
        if job == "None":
            jobmulti = 1.0
            job = "Unemployed"
        else: jobmulti = db.getjobs[job] / 100
        # REMOVE SERVER MULTIPLIER IN DMS
        multis = self.bot.db.getmultis(user.id, ctx.guild.id)
        embed = self.bot.fn.embed(f"{user.display_name}'s multipliers:",
                f"Personal Multiplier: `x{multis[0]}`\n"
                f"Server Multiplier: `x{multis[1]}`\n"
                f"**{job}** Multiplier: `x{jobmulti}`")
        await ctx.send(embed=embed)

    """
    @commands.command(name="baltop")
    async def _BalTop(self, ctx):
        async with ctx.channel.typing():
            #c.execute("SELECT user_id, balance FROM users
            #    ORDER BY balance DESC LIMIT 5")
            for rank, row in enumerate(c):
                user_id, balance = row
                user_name = str(self.bot.get_user(user_id))
                msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)

    @commands.command(name="debttop")
    async def _DebtTop(self, ctx):
        async with ctx.channel.typing():
            for rank, row in enumerate(c):
                user_id, balance = row
                user_name = str(self.bot.get_user(user_id))
                msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)

    @commands.command(name="nettop")
    async def _NetTop(self, ctx):
        async with ctx.channel.typing():
            for rank, row in enumerate(c):
                user_id, balance = row
                user_name = str(self.bot.get_user(user_id))
                msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)
    """
    
def setup(bot):
    bot.add_cog(economy(bot))
