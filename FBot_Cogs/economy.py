from discord.ext import commands
from triggers import tr
import discord
import asyncio
import sqlite3
import random
import dbfn

f = "~~f~~ "
# TIER ONE
t1jobs = {"Unemployed": [1000, "Take those government benefits"], # No degree, starting job
          "Scarecrow": [8000, "The birds. THEY FEAR ME"],
          "Factory Worker": [10000, "难以制作手机"],
          "Cleaner": [12000, "Don't touch my sheet"],
          "Plumber": [15000, "This job's pretty shitty if I'm being honest"]}
t1degrees = {"Standing": [2, 1.01, "Scarecrow"],
             "Birth Control": [3, 1.05, "Factory Worker"],
             "Cleaning": [4, 1.1, "Cleaner"],
             "Shittery": [5, 1.15, "Plumber"]}
# TIER TWO
t2jobs = {"Undertaker": [20000, "Sometimes when I bury bodies it wasn't because I committed a crime"],
          "Artist": [25000, "I'm actually not an artist; I've been framed"],
          "Nudist": [30000, "Stop being so clothed minded"],
          "Licensed Virgin": [3500, "The only difference is now you get paid for it"]}
t2degrees = {"Undertaking": [8, 1.25, "Undertaker"],
             "Art": [8, 1.3, "Artist"],
             "Feet Pics": [8, 1.35, "Nudist"],
             "Being yourself": [8, 1.4, "Licensed Virgin"]}
# TIER THREE
t3jobs = {"Pizza Delivery Guy": [5000, "The better the day the less we get paid"],
          "Offical Bread Taster": [60000, "You can't taste the bread, until you've touched the bread"],
          "The Milkman": [70000, "I am the milkman, my milk is delicious"],
          "Ass Waxer": [80000, "Feel the ass, wax the ass"]}
t3degrees = {"Pizza Making": [10, 1.5, "Pizza Delivery Guy"],
             "Bread Baking": [12, 1.6, "Offical Bread Taster"],
             "Milk Shaking": [14, 1.7, "The Milkman"],
             "Ass Quaking": [16, 2.8, "Ass Waxer"]}
# TIER FOUR
t4jobs = {"Professional Redditor": [100000, "Although life is tough, remember that it's not worth living"],
          "Discord Mod": [110000, "You're not a pedo 'til you're charged"],
          "Cocaine Man": [140000, "They misspelled my job title, I sell propane"],
          "Propane Man": [150000, "They misspelled my job title, I sell cocaine"]}
t4degrees = {"Obesity": [18, 2.0, "Professional Redditor"],
             "Predatory Behaviours": [18, 2.15, "Discord Mod"],
             "Selling Propane": [18, 2.35, "Cocaine Man"],
             "Selling Propane": [18, 2.5, "Propane Man"]}
# TIER FIVE
t5jobs = {"Psychic": [200000, "Professional four-chin teller"],
          "Loan Shark": [250000, "Suprisingly I still get debt"],
          "Sociopath": [300000, "Feelings? Like with your fingers?"],
          "Politician": [350000, "I love black people, hell my best friend is black!"]}
t5degrees = {"Bullshitting": [22, 2.7, "Psychic"],
             "Baiting": [24, 2.9, "Loan Shark"],
             "Politics": [26, 3.1, "Sociopath"],
             "Sociopathy": [26, 3.1, "Politician"]}
# TIER SIX
t6jobs = {"Resposible Inheriter": [500000, "Your job is to 'borrow' money from your rich and dying relatives"], # No degree
          "Irresposible Inheriter": [600000, "Similar to resposible inheriter but with the mindset: budget funerals are the way to go!"], # Becomes responsible
          "NOT CREATED YET": [700000, "NOT CREATED YET"],
          "NOT CREATED YET": [800000, "NOT CREATED YET"]}
t6degrees = {"Funding Trust": [30, 3.5, "Resposible Inheriter"],
             "Trust Funding": [32, 3.6, "Irresposible Inheriter"],
             "NOT CREATED YET": [34, 100, "NOT CREATED YET"],
             "NOT CREATED YET": [36, 100, "NOT CREATED YET"]}
# TIER SEVEN
t7jobs = {"Crime Lord": [100000, "Even crime lords need a degree in crime lording"],
          "Dictator": [2000000, "My people have freedom. Freedom to do what I tell them"],
          "Literally Hitler": [5000000, "I was not framed"],
          "NOT CREATED YET": [10000000, "NOT CREATED YET"]}
t7degrees = {"Crime Lording": [40, 4, "Crime Lord"],
             "Freedom": [44, 4.5, "Dictator"],
             "Ex-Artistry": [48, 5, "Literally Hitler"],
             "NOT CREATED YET": [52, 100, "NOT CREATED YET"]}
# TIER EIGHT
t8jobs = {"NOT CREATED YET": [50000000, "NOT CREATED YET"],
          "NOT CREATED YET": [100000000, "NOT CREATED YET"],
          "NOT CREATED YET": [200000000, "NOT CREATED YET"],
          "NOT CREATED YET": [400000000, "NOT CREATED YET"]}
t8degrees = {"NOT CREATED YET": [56, 100, "NOT CREATED YET"],
             "NOT CREATED YET": [60, 100, "NOT CREATED YET"],
             "NOT CREATED YET": [64, 100, "NOT CREATED YET"],
             "NOT CREATED YET": [70, 100, "NOT CREATED YET"]}
# TIER NINE
t9jobs = {"NOT CREATED YET": [800000000, "NOT CREATED YET"], # CEO
          "Billionare": [1000000000, "The description is in the job title"],
          "Rick Roller": [2000000000, "Back in the golden days of the 'net..."], # Special Rick Roll Command
          "FBot Develolper": [0, "a c c u r a t e"]} # Can't gain any debt # Gets a nice golden colour on their embeds, also FBot addresses them as Lord}
t9degrees = {"NOT CREATED YET": [80, 100, "NOT CREATED YET"],
             "Becoming Rich Quik": [85, 8, "Billionare"],
             "Trolling": [90, 9, "Rick Roller"],
             "Clicky-Clacky Keyboard Pressing": [100, 10, "FBot Develolper"]}

jobs = [t1jobs, t2jobs, t3jobs, t4jobs, t5jobs, t6jobs, t7jobs, t8jobs, t9jobs]
degrees = [t1degrees, t2degrees, t3degrees, t4degrees, t5degrees, t6degrees, t7degrees, t8degrees, t9degrees]

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
            user = message.author
            if user.bot: return
            if not commands.bot_has_permissions(send_messages=True): return
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
        job = profile[4]
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

    @commands.command(name="gift")
    @commands.is_owner()
    async def _Gift(self, ctx, amount, user: discord.User=None):
        if not user: user = ctx.author
        self.bot.db.updatebal(user.id, amount)
        await ctx.send("Lucky you")

    @commands.command(name="jobs")
    async def _Jobs(self, ctx):
        db = self.bot.db

        i = 1
        book = dbfn.reactionbook(self.bot, ctx)
        for tier in jobs:
            tiercopy = {}
            for job in tier:
                out = ["**"]
                if db.getjob(ctx.author.id) in [job]:
                    quals = ["📝"]
                elif job in db.getjobs(ctx.author.id):
                    quals = ["🔓"]
                else:
                    quals,  out = ["🔒"], ["~~"]
                tiercopy[job] = tier[job] + quals + out
            book.createpages(tiercopy, LINE=f"%2 %3%l%3 - {f}%0\n*%1*\n",
                             SUBHEADER=f"**FBot Jobs - Tier {i}**\n")
            i += 1
        await book.createbook(COLOUR=self.bot.fn.red)

    @commands.command(name="degrees")
    async def _Degrees(self, ctx):
        db = self.bot.db

        i = 1
        book = dbfn.reactionbook(self.bot, ctx)
        for tier in degrees:
            tiercopy = {}
            for degree in tier:
                out = ["**"]
                if degree == db.getdegree(ctx.author.id):
                    reqs = ["📝"] 
                elif tier[degree][2] in db.getjobs(ctx.author.id):
                    reqs = ["✅"]
                elif db.getusermulti(ctx.author.id) >= tier[degree][1]:
                    reqs = ["🔓"]
                else:
                    reqs, out = ["🔒"], ["~~"]
                tiercopy[degree] = tier[degree] + reqs + out
            book.createpages(tiercopy, LINE=f"%3 %4%l%4\n"
                             "Course length: `%0`, Requires `x%1` multiplier\n",
                             SUBHEADER=f"**FBot Degrees - Tier {i}**\n")
            i += 1
        await book.createbook(COLOUR=self.bot.fn.red)

    @commands.command(name="apply")
    async def _Apply(self, ctx, *, job):
        for jobname in jobnames:
            if job.lower() == jobname.lower():
                job = jobname
                break
        if job == "Unemployed":
            message = "You can apply to be unemployed, just `FBot resign"
        elif job in jobnames:
            db = self.bot.db
            user = ctx.author
            if job in db.getjobs(user.id):
                if db.getjob(user.id) == "Unemployed":
                    db.changejob(user.id, job)
                    db.worked(user.id)
                    embed = self.bot.fn.embed(f"You have been given the job: `{job}`",
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
        for degreename in degreenames:
            if degree.lower() == degreename.lower():
                degree = degreename
                break
        if degree in degreenames:
            db = self.bot.db
            user = ctx.author
            if db.getusermulti(user.id) >= degreenames[degree][1]:
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

    @commands.command(name="resign")
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

    @commands.command(name="drop")
    async def _Drop(self, ctx):
        db = self.bot.db
        degree = db.getdegree(ctx.author.id)
        if degree != "None":
            db.drop(ctx.author.id)
            message = f"You have dropped **{degree}**\nYou may take it again at anytime"
        else:
            message = "You have can't resign, you're unemployed!"
        await ctx.send(message)

    @commands.command(name="work")
    async def _Work(self, ctx):
        db = self.bot.db
        user = ctx.author
        if db.canwork(user.id):
            job = db.getjob(user.id)
            tax = random.uniform(0.1, 0.5) * 100

            if job == "Unemployed": jobmulti = 1.0
            else: jobmulti = db.getjobmulti(user.id) / 100

            salary = jobnames[job][0]
            if str(ctx.channel.type) == "private":
                salary *= db.getusermulti(user.id)
            else:
                multis = db.getmultis(user.id, ctx.guild.id)
                salary *= multis[0] * multis[1]

            income = round(salary * (tax / 100))
            balance = db.work(user.id, job, income)
            embed = self.bot.fn.embed("FBot work",
                    f"You work and earn: **{f}{round(salary)}**\n"
                    f"After {100 - round(tax)}% tax deductions: **{f}{income}**\n"
                    f"Your new balance is: **{f}{balance}**")
            await ctx.send(embed=embed)
            # Chance of debt collectors
        else:
            wait = db.lastwork(user.id)
            await ctx.send(f"You must wait another {wait} mins to work again")

    @commands.command(name="study")
    async def _Study(self, ctx):
        db = self.bot.db
        user = ctx.author
        if db.canstudy(user.id):
            degree = db.getdegree(user.id)
            if degree == "None":
                await ctx.send("You're not taking a degree right now")
                return
            salary = jobnames[db.getjob(user.id)][0]
            debt = round(salary * random.uniform(0.05, 0.4))
            
            progress = db.study(user.id, debt)
            length = degreenames[degree][0]
            if progress == length:
                db.finishdegree(user.id)
                db.startjob(user.id, degreenames[degree][2])
                embed = self.bot.fn.embed("Degree completed!",
                        f"You studied and gained debt: **{f}{round(debt)}**\n"
                        f"You may now apply for the **{degreenames[degree][2]}** job")
            else:
                db.studied(user.id)
                embed = self.bot.fn.embed(f"You studied for **{degree}**",
                        f"You studied and gained debt: **{f}{debt}**\n"
                        f"Degree course progress: `{progress}/{length}`")
            await ctx.send(embed=embed)
            # Chance of debt collectors
        else:
            wait = db.laststudy(user.id)
            await ctx.send(f"You must wait another {wait} mins to study again")

    @commands.command(name="balance", aliases=["bal"])
    async def _Balance(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        bal, debt = db.getbal(user.id)
        embed = self.bot.fn.embed(f"{user.display_name}'s balance",
                f"FBux: **{f}{bal}**\n"
                f"Debt: **{f}{debt}**")
        await ctx.send(embed=embed)

    @commands.command(name="multis", aliases=["multipliers"])
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
        embed = self.bot.fn.embed(f"{user.display_name}'s multipliers:",
                message + f"\n{job} Multiplier: `x{jobmulti}`")
        await ctx.send(embed=embed)
    
    @commands.command(name="top")
    @commands.cooldown(1, 10, type=commands.BucketType.user)
    async def _Top(self, ctx, toptype):
        if toptype in ["bal", "netbal", "debt", "netdebt", "multi", "servmulti"]:
            message = ""
            async with ctx.channel.typing():
                results = self.bot.db.gettop(toptype)
                for rank, row in results:
                    ID, typeitem = row
                    if toptype == "servmulti":
                        try: name = self.bot.get_guild(ID).name
                        except: name = "Server"
                    else:
                        try: name = self.bot.get_user(ID).display_name
                        except: name = "User"
                    if toptype in ["bal", "netbal", "debt", "netdebt"]:
                        if typeitem == 0: break
                        message += f"{rank+1}. {name}: **{f}{typeitem}**\n"
                    elif toptype == "multi":
                        if typeitem == 10000: break
                        message += f"{rank+1}. {name}: `x{typeitem/10000}`\n"
                    else:
                        if typeitem == 1000000: break
                        message += f"{rank+1}. {name}: `x{typeitem/1000000}`\n"
            embed = self.bot.fn.embed(f"FBot Top {toptype}", message)
            await ctx.send(embed=embed)
        else: await ctx.send("We don't have a leaderboard for that...")

    @commands.command(name="store", aliases=["shop"])
    async def _Store(self, ctx):
        await ctx.send("This feauture is still in development")
    
def setup(bot):
    bot.add_cog(economy(bot))
