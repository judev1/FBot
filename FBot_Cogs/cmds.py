from discord.ext import commands
from dbfn import reactionbook

cmdpages = ("""**Write `FBot ` (the prefix) however you want, I don't care**
*If you ever lose your prefix use plain* `prefix` *to get it*
*Shorthands for this command are:* `commands`/`cmds`

 Page 1: **Contents**
 Page 2: **General Commands**
 Page 3: **NEW Economy Commands**
 Page 4: **Fun Commands**
 Page 5: **Counting Commands**
 Page 6: **Infomation Commands**
 Page 7: **Link Commands**""",

"""**General Commands**

`on`/`off`: *Toggles FBot in the channel*
`modtoggle` `on`/`off`: **ADMIN ONLY** *Allows only admin to toggle FBot*
`respond` `few`/`some`/`all`: **ADMIN ONLY** *Changes the amount of triggers FBot responds to*
`prefix` `reset`/`<newprefix>`: **ADMIN ONLY** *Resets or changes FBot's prefix*

`status`: *Gives a basic overview of FBot in the current channel*
`status` `server`: *Gives an overview of FBot for the server*
`status` `server` `mod`: **ADMIN ONLY** *Displays the status for hidden channels too*

`help`: *Gives some helpful links and commands*
`snipe` `(number)`: *Get the last number of editted and deleted messages, up to 10*
`purge`/`thanos` `<number>`: **ADMIN ONLY** *Deletes a number of messages*""",

"""**Economy Commands**

`economy`: *Gives a handy guide to FBot's economy system*
`profile` `(@member)`: *Shows the profile of a member*

`work`: *Allows you to work to earn that sweet sweet cash*
`study`: *Work towards completing your degree*

`jobs`: *Lists all jobs*
`degrees`: *Lists all degrees*

`apply` `<job>`: *Apply for a job*
`take` `<degree>`: *Apply for a degree*

`resign`: *Resign from your current job*
`drop`: *Drop your current degree*

`bal`/`balance` `(@member)`: *Shows the balance of a member*
`multis`/`multipliers` `(@member)`: *Shows the multipliers for a member*

`top` `bal`/`netbal`/`debt`/`netdebt`: Shows the top users in an area""",

"""**Fun Commands**

`bonk` `@user`/`image url`: *BONK*
`bigpp` `@user`/`image url`: *Who's got a big pp?*

`ppsize` (`@member`): *Gets a members actual ppsize*
`fball`/`8ball` <question>: *Ask FBot (and you don't need to you the prefix!)*
`say` `<message>`: *Makes FBot say whatever you want*
`dm`/`dms`: *Bring FBot into your DMs, why? Who knows!*

**NEW Minigames**

`snake`: *Play our very own discord snake game for FBux*""",

"""**Counting Commands**

`counter`/`counting`: **ADMIN ONLY** *Sets the current channel to the counting channel*
`number`/`last`: *Gets the last number for counting*
`hs`/`highscores`: *Gets the counting highscores*""",

"""**Infomation Commands**

`info`: *Displays some infomation about the FBot*
`serverinfo`: *Displays infomation about the server*
`stats`: *Shows message stats for FBot in  a peroid*

`session`/`uptime`: *Gives a session overview*
`version`/`ver`: *Shows the version of the bot*
`ping`: *Shows the current ping for the bot*

`events`/`event`: *Shows any events that are running and gives an overview of it*
`notices`/`notice`: *Shows some cool stuff :)*
`cl`/`cls`/`changelogs` (`<ver>`/`list`/`recent`): *Gets changelogs*""",

"""**Link Commands**

`links`: *Gives all links*
`vote`: *Gives a link to vote for this FBot*
`invite`: *Gives a link to invite FBot to your server*
`Github`: *Gives a link to view FBots Github page*
`Top.gg`/`Topgg`: *Gives a link to view FBots Top.gg page*
`server`: *Gives a link to join FBots server*
`Minecraft`/`MC`: *Gives infomation to join our MC server*""")

devcmdpage = ["""**General Commands**
`devon`/`devoff`: *Toggles FBot*
`devmodtoggle` `on`/`off`: *Allows only admin to toggle FBot*
`treload`: *Reloads Trigger.csv*
`eval` `<to eval>`: *Evaluates content*
`host`: *The name of the computer FBot is running on*

**Cog Commands**
`reload` `<cog>`: *Reloads a cog*
`load` `<cog>`: *Loads a cog*
`unload` `<cog>`: *Unloads a cog*

**Server Commands**
`servers`/`members`: *Gives a neat little overview of all the servers FBot is in*
`search` `<query>`: *Searches for a server name*
`lookup` `<server_id>`: *Gives an overview of a server*
`newinvite` `<server_id>`: *Creates a temporary invite for the server*

**Misc**
`devsetnumber` `<number>`: *Manually sets the counting number in a server*
`presence` `<newpresence>`: *Changes FBot's presence*
`send` `<channel_id>` `<message>`: *Sends a message to a channel*
`dmuser` `@user` `<message>`: *Sends a message to a user*"""]

ehelp = ["""**Basic Overview**
Welcome to FBot's economy! This will be your guide to FBot economy system.
Firstly the big question, how do you earn money? To earn money, or FBux,
indicated by this symbol: ' ~~f~~ ', you must work.

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
and want to pick a new one, or if your degree really isn't SOMETHING your fancy,
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

**Competitive**
It's no fun winning and not knowing it, know it. Use `FBot baltop` to view the
richest FBoters and `FBot debttop` to view the most in debt. With more to come,
stay posted.

**Store**
Use your money, to get... more money. Learn how to commit tax evasion or money
laundering, or whatever else we choose to add! What better way to invest your
hard earned cash, than in more cash and future content!

**Suggestions**
We are always working on new ways to improve FBot, if you have any suggestions,
or just wanna drop by for a chat, use `FBot server` to join our server.

**Extra**
Currently there is no way to remove debt, but since it doesn't cause you any
harm, you'll just have to learn to live with it."""]

class cmds(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.red = bot.fn.red
        
    @commands.command(name="commands", aliases=["cmds"])
    async def _Commands(self, ctx, *page):
        book = reactionbook(self.bot, ctx, TITLE="FBot Help")
        book.createpages(cmdpages, ITEM_PER_PAGE=True)
        await book.createbook(MODE="numbers", COLOUR=self.red)

    @commands.command(name="devcmds")
    @commands.is_owner()
    async def _DevCommands(self, ctx):
        book = reactionbook(self.bot, ctx, TITLE="FBot Dev Commands")
        book.createpages(devcmdpage)
        await book.createbook(MODE="numbers", COLOUR=self.red)

    @commands.command(name="economy")
    async def _Economy(self, ctx):
        book = reactionbook(self.bot, ctx, TITLE="FBot Economy")
        book.createpages(ehelp, ITEM_PER_PAGE=True)
        await book.createbook(MODE="numbers", COLOUR=self.red, TIMEOUT=60)

def setup(bot):
    bot.add_cog(cmds(bot))
