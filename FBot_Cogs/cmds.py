from discord.ext import commands
from dbfn import reactionbook

cmdpages = ("""**Write `FBot ` (the prefix) however you want, I don't care**
*If you ever lose your prefix use plain* `prefix` *to get it*

 Page 1: **Contents**
 Page 2: **General Commands**
 Page 3: **NEW Economy Commands**
 Page 4: **Fun Commands**
 Page 5: **Counting Commands**
 Page 6: **Information Commands**
 Page 7: **Link Commands**""",

"""**General Commands**

`on | off`:
*The best decision you'll make - no I'm not going to specify which one I mean*
`modtoggle [on | off]`: **ADMIN ONLY**
*Makes FBot only toggleable for mods so pesky members aren't turning it off when you're not around*
`respond [few | some | all]`: **ADMIN ONLY**
*Changes how often FBot responds to messages*
`prefix [<newprefix> | reset]`: **ADMIN ONLY**
*Allows you to change the prefix for FBot*

`status`:
*Gives FBots status for the channel (whether it is set to on or off), along with how its modtoggle and respond values*
`status server`:
*Just like FBot status except it shows the status for every channel*
`status server mod`: **ADMIN ONLY**
*Just like FBot status server except it shows the status for hidden channels, in most cases all channels are hidden*

`help`:
*Returns some basic links and commands to get you started*
`cmds`:
*View all the commands that you see here, incredibly meta*

`snipe (<number>)`:
*Get up to ten of the last x edited and deleted messages in a channel*
`purge <number>`: **ADMIN ONLY**
*Also known as thanos, deletes x amount of messages in the channel*""",

"""**Economy Commands**

`economy`: **NEW**
*Gives you all the information about economy found on the economy page*
`profile (@member)`: **NEW**
*Returns your economy profile, or anyone else whom you specify*
`store`: **NEW**
*Not yet implemented*

`work`: **NEW**
*Can be used once an hour to earn that sweet sweet cash, after tax of course*
`study`: **NEW**
*Can be used once an hour to progress your degree (and eventually unlock a new job)*

`jobs`: **NEW**
*Returns a list of degrees, modified so that it's relevent to you*
`degrees`: **NEW**
*Returns a list of degrees, modified so that it's relevent to you*

`apply` `<job>`: **NEW**
*Apply for a job, you must unlock the relative degree first*
`take` `<degree>`: **NEW**
*Take a degree, you must have a high enough multiplier first*

`resign`: **NEW**
*Quit your current job, great for slackers and those changing jobs*
`drop`: **NEW**
*Had enough of you're degree? Drop it! But be careful, all your progress for that degree will be lost*

`bal (@member)`: **NEW**
*Shows your balance or that of a member*
`multis (@member)`: **NEW**
*Shows your multipliers or a members*
`top [bal | netbal | debt | netdebt | multi | servmulti]`: **NEW**
*Shows the top for a type. more to be added""",

"""**Fun Commands**

`bigpp [@user | <image url>]`:
*Bonks a member or image which you deem unworthy*
`bonk [@user | <image url>]`:
*Generates an image with big pp energy about a member or image you specify*

`ppsize (@member)`:
*Gets your actual ppsize, no joke*
`fball <question>`:
*Ask FBot. Can be used without the prefix for your FBotting pleasure*
`say <message>`:
*Commit identity fraud and speak as FBot, don't worry FBot removes all evidence*
`dms`:
*Invite FBot to your DMs - for all the conversations you'd rather have in private*

**Minigames**

`snake`: **NEW**
*Play the snake game, in Discord, with FBot. Yes, that sentence was epic*""",

"""**Counting Commands**

`counting`: **ADMIN ONLY**
*Sets the current channel to the counting channel, useful if you don't have a counting channel*
`number | last`:
*Gets the last number, and last counter, especially good when dealing with tampering*
`hs`/`highscores`:
*Displays the highscores in counting for the top servers*""",

"""**Information Commands**

`info`: *Displays some infomation about the FBot*
`serverinfo`: *Displays infomation about the server*
`stats`: *Shows message stats for FBot in  a peroid*

`session`/`uptime`: *Gives a session overview*
`version`/`ver`: *Shows the version of the bot*
`ping`: *Shows the current ping for the bot*

`events`/`event`: *Shows any events that are running and gives an overview of it*
`notices`/`notice`: *Shows some cool stuff :)*
`cl`/`cls`/`changelogs` (`<ver>`/`list`/`recent`):
*Gets changelogs*""",

"""**Link Commands**

`links`:
*Gives you every link that we have clickable, inlcuding our website, github and more*
`vote`:
*Gives links to vote for FBot*
`invite`:
*Gives you a link to invite FBot to your server*
`server`:
*Gives a link to join our server*""")

devcmdpage = ["""**General Commands**
`devon`/`devoff`
`devmodtoggle [on | off]`

`eval <to eval>`
`await <function> <to await>`

`reload` `<cog>`: *Reloads a cog*
`load` `<cog>`: *Loads a cog*
`unload` `<cog>`: *Unloads a cog*

`servers`/`members` (broken)
`search <query>`
`lookup <server_id>`
`newinvite <server_id>`

`host`
`treload`
`devsetnumber <number>`
`presence <newpresence>`
`send <channel_id> <message>`
`dmuser @user <message>`"""]

class cmds(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.red = bot.fn.red
        
    @commands.command(name="commands", aliases=["cmds"])
    async def _Commands(self, ctx, *page):
        book = reactionbook(self.bot, ctx, TITLE="FBot Commands")
        book.createpages(cmdpages, ITEM_PER_PAGE=True)
        await book.createbook(MODE="numbers", COLOUR=self.red)

    @commands.command(name="devcmds")
    @commands.is_owner()
    async def _DevCommands(self, ctx):
        book = reactionbook(self.bot, ctx, TITLE="FBot Dev Commands")
        book.createpages(devcmdpage)
        await book.createbook(MODE="numbers", COLOUR=self.red)

def setup(bot):
    bot.add_cog(cmds(bot))
