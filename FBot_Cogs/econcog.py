from discord.ext import commands
from functions import cooldown
from triggers import tr
import commands as cm
import economy as e
import discord

f = "~~f~~ "

class fakeuser: id = 0
user = fakeuser()

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.voteschannel = self.bot.get_channel(757722305395949572).send

    @commands.command(name="profile")
    @commands.check(cooldown)
    async def _Profile(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        profile = list(db.getprofile(user.id))
        job = profile[4]
        if profile[5] == "None":
            degree = "No degree"
        else:
            degree = profile[5]
            degree = f"{degree} - {profile[6]}/{e.courses[degree][0]}"
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s profile:")
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
    @commands.check(cooldown)
    async def _Gift(self, ctx, amount, user: discord.User=None):
        if not user: user = ctx.author
        self.bot.db.updatebal(user.id, amount)
        await ctx.send("Lucky you")        

    @commands.command(name="scheme")
    @commands.check(cooldown)
    async def _Scheme(self, tx):
        db = self.bot.db
        user = ctx.author
        
    @commands.command(name="bal")
    @commands.check(cooldown)
    async def _Balance(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        bal, debt = db.getbal(user.id)
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s balance",
                f"FBux: **{f}{bal}**", f"Debt: **{f}{debt}**")
        await ctx.send(embed=embed)

    @commands.command(name="multis")
    @commands.check(cooldown)
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

    @commands.command(name="inv")
    @commands.check(cooldown)
    async def _Inventory(self, ctx):
        return
        await ctx.send(embed=embed)
    
    @commands.command(name="top")
    @commands.check(cooldown)
    async def _Top(self, ctx, toptype):
        if toptype == "netbal":
            toptype = "netfbux"
        if toptype in ["bal", "netfbux", "debt", "", "multi", "servmulti"]:
            message = ""
            async with ctx.channel.typing():
                results = self.bot.db.gettop(toptype)
                for rank, row in results:
                    ID, typeitem = row
                    if toptype == "servmulti":
                        try: name = self.bot.get_guild(ID).name
                        except: name = "Server"
                    else:
                        try: name = await self.bot.fetch_user(ID).name
                        except: name = "User"
                    if toptype in ["bal", "netfbux", "debt", "netdebt"]:
                        if typeitem == 0: break
                        message += f"{rank+1}. {name}: **{f}{typeitem}**\n"
                    elif toptype == "multi":
                        if typeitem == 10000: break
                        message += f"{rank+1}. {name}: `x{typeitem/10000}`\n"
                    else:
                        if typeitem == 1000000: break
                        message += f"{rank+1}. {name}: `x{typeitem/1000000}`\n"
            embed = self.bot.fn.embed(ctx.author, f"FBot Top {toptype}", message)
            await ctx.send(embed=embed)
        else: await ctx.send("We don't have a leaderboard for that...")

    @commands.command(name="store")
    @commands.check(cooldown)
    async def _Store(self, ctx):
        await ctx.send("This feature is still in development")

    @commands.command(name="vote")
    @commands.check(cooldown)
    async def _Vote(self, ctx):
        fn, db = self.bot.fn, self.bot.db
        user = ctx.author
        job = db.getjob(user.id)
        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)
        salary = e.salaries[job] * jobmulti
        salary *= db.getusermulti(user.id)
        
        embed = fn.embed(user, "FBot Vote",
                         "If you vote you'll earn your salary without tax",
                         f"So **~~f~~ {round(salary)}** if I'm not mistaken",
                         "AND multiplier worth x20 that of using a trigger\n",

                         f"[Top.gg vote]({fn.votetop})",
                         f"[discordbotlist]({fn.votedbl}) (No rewards yet)")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        db = self.bot.db
        user_id = data["user"]
        db.register(user_id)
        try: name = await self.bot.fetch_user(user_id).name
        except: name = "User"
            
        embed = self.bot.fn.embed(user, "Tog.gg test",
                                  f"{name} tested out the webhook")
        await self.voteschannel(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        db = self.bot.db
        user_id = data["user"]
        db.register(user_id)
        try: name = await self.bot.fetch_user(user_id).name
        except: name = "User"
        
        job = db.getjob(user_id)
        if job == "Unemployed": jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user_id)
        salary = jobnames[job][0] * jobmulti
        salary = round(salary * db.getusermulti(user_id))
        db.updatebal(user_id, salary)

        bonus = 1
        if self.bot.ftime.isweekend(): bonus = 2
        db.increasemultiplier(user_id, 0, 20 * bonus)
            
        embed = self.bot.fn.embed(user, "Tog.gg vote",
                                  f"{name} voted and gained **~~f~~ {salary}**")
        await self.voteschannel(embed=embed)
    
def setup(bot):
    bot.add_cog(economy(bot))
