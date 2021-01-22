import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
import sqlite3
import random
from functions import fn

conn = sqlite3.connect("economy.db")
f = "~~f~~ "

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        # Create blank tables if they don't exit
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id integer NOT NULL,
            balance integer NOT NULL,
            networth integer NOT NULL,
            netdebts integer NOT NULL)""")
        conn.commit()

        # Add any users not already in DB
        c = conn.cursor()
        for user in self.bot.users:
            t = (user.id,)
            c.execute("SELECT 1 FROM users WHERE user_id=?", t)
            if not c.fetchone():
                c.execute("INSERT INTO users VALUES(?, 0, 0, 0)", t)
        conn.commit()

    @commands.command(name="balance", aliases=["bal"])
    async def get_balance(self, ctx, mention: discord.Member=None):
        # Get a users balance
        # fbot bal, or fbot bal @mention
        if mention:
            user_id = mention.id
        else:
            user_id = ctx.author.id
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
        t = (new_balance, mention.id,)
        c = conn.cursor()
        c.execute("""UPDATE users SET balance=?
            WHERE user_id=?""", t)
        conn.commit()
        await ctx.message.add_reaction("✅")

    @commands.command(name="baltop")
    async def get_baltop(self, ctx):
        # Gets top balances
        # `fbot baltop`
        await ctx.trigger_typing()
        msg = "Top balances:"
        c = conn.cursor()
        c.execute("""SELECT user_id, balance FROM users
            ORDER BY balance DESC LIMIT 5""")
        for rank, row in enumerate(c):
            user_id, balance = row
            user_name = str(self.bot.get_user(user_id))
            msg += f"\n{rank+1}. {user_name}: {f}{balance}"
        await ctx.send(msg)

    # networthtop

    # debttop

    @commands.command(name="work")
    async def do_work(self, ctx):
        # Work for cash
        # Get 500 to 1000 credits then lose 80% to 90% of it due to income tax
        # (cooldown 4 hours)
        # `fbot work`
        income = random.randint(500, 1000)
        taxed_income = int(income * random.uniform(0.1, 0.2)) # lose 80% to 90%
        t = (taxed_income, ctx.author.id,)
        c = conn.cursor()
        c.execute("UPDATE users SET balance=balance+? WHERE user_id=?", t)
        conn.commit()
        t = (ctx.author.id,)
        c.execute("SELECT balance FROM users WHERE user_id=?", t)
        new_balance = c.fetchone()[0]
        await ctx.send(f"You worked and got paid {f}{income}.\n"
            f"After calculating tax, you keep {f}{taxed_income}.\n"
            f"New balance: {f}{new_balance}")
    
def setup(bot):
    bot.add_cog(economy(bot))
