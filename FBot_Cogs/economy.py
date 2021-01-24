from discord.ext import commands
from discord.ext.commands import MemberConverter
import sqlite3
import random
import discord

f = "~~f~~ "
jobs = {# TIER ONE
        "Unemployed": (1000, "You gotta dismantle the government somehow"), # No degree, starting job
        "Waitor": (8000, "This seems like a good idea you said, I'll enjoy this a lot you said"),
        "Janitor": (10000, "They ask you how you are, and you just have to say you're fine when you're not really fine, but you just can't get into it, because they would never understand"),
        "Plumber": (15000, "Just because you're not a janitor doesn't mean I'll let you near my kids"),

        # TIER TWO
        "Loan Shark": (20000, "No one can escape debt, **no one**"),
        "Physic": (25000, "I only work 9 to 5, except between 10 to 3 when I'm having lunch, and I'm available all weekdays, except for Monday, Wednesday, Thursday and Friday, that'll be 25000 for the first session and you'll need to pay for the next 8 seesions, with intrest of course. So when can I expect to see you?"),
        # TIER FIVE

        # TIER SIX
        "Resposible Inheriter": (50000000, "Your job is to recieve money from your rich and dying relatives"), # No degree
        "Irresposible Inheriter": (100000000, "Similar to resposible inheriter but with the mindset: Budget funerals are the way to go!"), # Becomes responsible
        
        # TIER SEVEN
        "Crime Lord": (200000000, "Even crime lords need a degree in crime lording"),
        
        # TIER EIGHT
        "Billionare": (1000000000, "The description is in the job title"),
        "FBot Deveolper": (0, "a c c u r a t e"), # Can't gain any debt # Gets a nice golden colour on their embeds, also FBot addresses them as Lord
        }
pjobs = {# PUNNISHMENT JOBS
         "Mormon": (-1000, "You devote your life to a good cause, for now at least"), # There is a chace you'll become enlightened whenever you switch jobs
         "Karen": (-5000, "Just great, now everyone hates you"), # When you have no debt and a lot of money (in tier 3)
         "Light Mode Enthusiast": (-50000, "Maybe if you stopped using discord light mode you might actually make some money"), # Not sure yet
         "Ex-FBot Deveolper": (-100000, "FBot has maintence costs, glad you noticed") # When you change jobs after being an FBot Developer
         }
# Option: Severs can turn off a feature called job-security which means you can gain a punishment job at anytime instead of just during switching jobs
degrees = {# TIER ONE
           "Food Touching": (4, multi, "Waitor"),
           "Touching": (7, multi, "Plumber"),
           "Touching Shit": (10, multi, "Janitor"),

           # TIER TWO
           "Baiting": (12, multi, "Loan Shark"),
           "Bullshittery": (15, multi, "Physic"),
           "UNDECIDED": (18, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),

           # TIER THREE
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),

           # TIER FOUR
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),

           # TIER FIVE
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),

           # TIER SIX
           "Funding Trust": (35, multi, "Iresposible Inheriter"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),

           # TIER SEVEN
           "Crime Lording": (30, multi, "Crime Lord"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),

           # TIER EIGHT
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "UNDECIDED": (35, multi, "UNDECIDED"),
           "Becoming Rich Quik": (180, multi, "Billionare"),
           "clicky-clacky keyboard pressing": (200, multi, "FBot Dev")
           }

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        fn, db = bot.fn, bot.db

        @self.bot.event
        def _Multiply(message):
            # TODO: Check if FBot can talk in channel
            commandcheck = content[len(fn.getprefix(self.bot, message)):]
            for command in self.bot.walk_commands():
                if commandcheck.startswith(command.name):
                    db.increaseusermultiplier(message.author.id, 2)
                    return
                for alias in command.aliases:
                    if commandcheck.startswith(alias):
                        db.increaseusermultiplier(message.author.id, 2)
                        return
            if str(message.channel.type) != "private":
                db.Add_Channel(message.channel.id, message.guild.id)
                priority = "all"
            else: priority = db.Get_Priority(message.guild.id)
            trigger_detected = tr.trigger_respond(message, priority)[0]
            if trigger_detected:
                db.increaseusermultiplier(message.author.id, 1)

    @commands.command(name="balance", aliases=["bal"])
    async def get_balance(self, ctx, mention: discord.Member=None):
        # Get a users balance
        # fbot bal, or fbot bal @mention
        if mention:
            user_id = mention.id
        else:
            user_id = ctx.author.id
        dbcheck(user_id)
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT balance FROM users WHERE user_id=?", t)
        balance = c.fetchone()[0]
        emb = fn.embed("Balance",f"{f}{balance}")
        await ctx.send(embed=emb)

    @commands.command(name="devsetbalance", aliases=["devsetbal"])
    @commands.is_owner()
    async def dev_set_balance(self, ctx, mention: discord.Member, new_balance: int):
        # [dev] set any users balance:
        # fbot devsetbalance @mention 1234
        # ONLY use this for testing, misuse may break something.
        dbcheck(user_id)
        t = (new_balance, mention.id,)
        c = conn.cursor()
        c.execute("""UPDATE users SET balance=?
            WHERE user_id=?""", t)
        conn.commit()
        await ctx.message.add_reaction("✅")

    async def _Profile(self, ctx, mention: discord.Member=None):
        if mention is None:
            user_id = ctx.author.id
        else: user_id = mention.id
        # GET BALANCE
        # GET NETWORTH
        # GET DEBT
        # GET NETDEBT
        # GET JOB # GET PAY
        # GET DEGREE # GET PROGRESS
        await ctx.send(f"Balance: {f}{balance}")

    @commands.command(name="multipliers", aliases=["multis"])
    async def _Multipliers(self, ctx, mention: discord.Member=None):
        if mention is None:
            user_id = ctx.author.id
        else: user_id = mention.id
        # GET USER MULTIPLIER
        # GET SKILL MULTIPLIER
        # GET SERVER MULTIPLIER
        await ctx.send(f"Balance: {f}{balance}")

    @commands.command(name="balance", aliases=["bal"])
    async def _Balance(self, ctx, mention: discord.Member=None):
        if mention is None:
            user_id = ctx.author.id
        else: user_id = mention.id
        # GET BALANCE
        # GET DEBT
        await ctx.send(f"Balance: {f}{balance}")

    @commands.command(name="baltop")
    async def _BalTop(self, ctx):
        async with ctx.channel.typing():
            #c.execute("""SELECT user_id, balance FROM users
            #    ORDER BY balance DESC LIMIT 5""")
            for rank, row in enumerate(c):
                user_id, balance = row
                user_name = str(self.bot.get_user(user_id))
                msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)

    @commands.command(name="debttop")
    async def _DebtTop(self, ctx):
        async with ctx.channel.typing():
            #c.execute("""SELECT user_id, balance FROM users
            #    ORDER BY balance DESC LIMIT 5""")
            for rank, row in enumerate(c):
                user_id, balance = row
                user_name = str(self.bot.get_user(user_id))
                msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)

    @commands.command(name="nettop")
    async def _NetTop(self, ctx):
        async with ctx.channel.typing():
            #c.execute("""SELECT user_id, balance FROM users
            #    ORDER BY balance DESC LIMIT 5""")
            for rank, row in enumerate(c):
                user_id, balance = row
                user_name = str(self.bot.get_user(user_id))
                msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)

    @commands.command(name="work")
    async def _Work(self, ctx):
        # Work for cash
        # Get 500 to 1000 credits then lose 80% to 90% of it due to income tax
        # (cooldown 2 hours)
        # `fbot work`
        dbcheck(user_id)
        income = random.randint(500, 1000)
        taxed_income = int(income * random.uniform(0.1, 0.2)) # lose 80% to 90%
        # UPDATE BALANCE
        t = (ctx.author.id,)
        c.execute("SELECT balance FROM users WHERE user_id=?", t)
        new_balance = c.fetchone()[0]
        await ctx.send(f"You worked and got paid {f}{income}.\n"
            f"After calculating tax, you keep {f}{taxed_income}.\n"
            f"New balance: {f}{new_balance}")
    
def setup(bot):
    bot.add_cog(economy(bot))
