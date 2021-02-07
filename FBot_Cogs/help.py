from discord.ext import commands
from dbfn import reactionbook
from functions import cooldown

ehelp = ["""**Overview**
Welcome to FBot's economy! This will be your guide to FBot economy system.
Firstly the big question, how do you earn money? To earn money, or FBux,
indicated by this symbol: ' ~~f~~ ', you must work.

 Page 1: **Overview**
 Page 2: **Introduction**
 Page 3: **Working, Studying and Multipliers**
 Page 4: **Information and More**""",

"""**Introduction**
Working is fairly straight forward, every hour you can take a work shift and
earn your jobs worth of money (minus tax). Now I bet that sounds pretty neat,
but with FBot's multi trillion dollar maintenance costs, we have to keep tax
high, so tax can be anywhere between 60% and 90%, depending on how lucky you
are. And just so you don't have to worry, tax comes straight off your paycheck,
how thoughtful! You'll never have to worry about ~~us taking it~~ forgetting to pay
it again!

Now we have a wide selection of jobs, but you can't just apply for any one of
them - you're not qualified! Silly you, you need to take a degree first. Degrees
you say? Well glad you asked, see you can take a degree which will allow you to
apply for a certain job. Easy? Not so fast. You won't be able to study any old
degree, majority of degrees start of as locked but you will gain access to more
and more of them as you interact with FBot. Done? Not quite. As you study for
your degree, which operates similarly to the work function, you will accumulate
debt, why? Who knows! To think you're only studying to pay more taxes in the
future ~~something isn't quite right here~~.""",

"""**Working and Studying**
To work and study use `FBot work` and `FBot study`. But wait... There's more.
To find jobs and degrees, you can use `FBot degrees` and `FBot jobs`. Now this
is just mind blowing, BUT THERE'S MORE! You can't just study without a degree,
so to take a degree or apply for a job use `FBot apply <job>` or `FBot take`
`<degree>`. Bet you weren't expecting that. One final point. If you have a job
and want to pick a new one, or if your degree really isn't to your liking,
you can drop it no questions asked. So that's `FBot resign` for jobs, and `FBot`
`drop` for degrees. Make sure you know what you're doing, because you won't be
able to recover your progress for degrees. There, I'm done.

**Multipliers**
Doesn't practise make perfect? Yes. Same applies for FBot, the more you spam,
the more your multipliers increase, the relevant ones at least. There are three
types of multipliers, first is your personal one. This multiplier follows you
everywhere. Every time you interact with FBot, even in DMs, this multiplier will
increase. Second is your server multiplier. This will increase as people
interact with FBot in a server, the more a server uses FBot, the higher the
multiplier increases by. Last there is your job multiplier. This is specific to
each job and increases every time you successfully work. Multipliers are used
to increase the amount of money you earn. Your personal multiplier can also
help you unlock new degree which in turn gives you access to new jobs.""",

"""**Information**
Wanna see your progress as a FBoter? Use `FBot profile`. Wanna laugh at inferior
mortals? Use `FBot profile @inferior mortal`. Wanna view your multipliers?
Use `FBot mutlis`. Want me to stop? No? That's what I thought. You can use
`FBot cmds` to view a full list of available commands.

**Competitive, Store, Suggestions and More!**
It's no fun winning and not knowing it, know it. Use `FBot baltop` to view the
richest FBoters and `FBot debttop` to view the most in debt. With more to come,
stay posted.

Use your money, to get... more money. Learn how to commit tax evasion or money
laundering, or whatever else we choose to add! What better way to invest your
hard earned cash, than in more cash and future content!

VOTE FOR FBOT and get your entire salary WITHOUT TAX, use `FBot vote` to find
out more.

We are always working on new ways to improve FBot, if you have any suggestions,
or just wanna drop by for a chat, use `FBot server` to join our server.

Currently there is no way to remove debt, but since it doesn't cause you any
harm, you'll just have to learn to live with it - for now."""]

class help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="help")
    @commands.check(cooldown)
    async def _Help(self, ctx):
        fn = self.bot.fn
        
        embed = fn.embed(ctx.author, "FBot Help",
                "**Useful Commands**",
                "Use `FBot on/off` to toggle fbot",
                "Use `FBot cmds` for a list of commands",
                "Use `FBot economy` for help with our currency\n",
                "**Useful Links**",
                f"[Invite FBot]({fn.top}) or "
                f"[join our server!]({fn.server})")

        await ctx.send(embed=embed)

    @commands.command(name="economy")
    async def _Economy(self, ctx):
        colour = self.bot.db.getcolour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Economy")
        book.createpages(ehelp, ITEM_PER_PAGE=True)
        await book.createbook(MODE="numbers", COLOUR=colour, TIMEOUT=60)

def setup(bot):
    bot.add_cog(help(bot))
