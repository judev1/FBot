from discord.ext import commands
from dbfn import reactionbook

cmdpages = ("""**Write `FBot ` (the prefix) however you want, I don't care**
*If you ever lose your prefix use plain* `prefix` *to get it*
*Shorthands for this command are:* `commands`/`cmds`

 Page 1: **Contents**
 Page 2: **General Commands**
 Page 3: **Infomation Commands**
 Page 4: **Link Commands**
 Page 5: **Fun Commands**
 Page 6: **Counting Commands**""",

"""**General Commands**

`on`/`off`: *Toggles FBot*
`help`/`?`: *Gives some helpful links and commands*
`modtoggle` `on`/`off`: **ADMIN ONLY** *Allows only admin to toggle FBot*
`prefix` `reset`/`<newprefix>`: **ADMIN ONLY** *Resets or changes FBot's prefix*
`status` `server`: *Gives an overview of the status for the server*
`status` `server` `mod`: **ADMIN ONLY** *Displays the status for hidden channels too*
`respond` `few`/`some`/`all`: **ADMIN ONLY** *Changes the amount of triggers FBot responds to*
`purge`/`thanos` `<number>`: **NEW ADMIN ONLY** *Deletes the last number of messages*""",

"""**Infomation Commands**

`info`: *Displays some infomation about the FBot*
`serverinfo`: *Displays infomation about the server*
`status`: *Displays the status of the bot in the current channel*
`session`/`uptime`: *Gives a session overview*
`version`/`ver`: *Shows the version of the bot*
`ping`: *Shows the current ping for the bot*
`events`/`event`: *Shows any events that are running and gives an overview of it*
`notices`/`notice`: *Shows some cool stuff :)*
`pn`/`pns`/`patchnotes` (`<ver>`/`list`/`recent`): *Gives you the patchnotes for a version*""",

"""**Link Commands**

`links`: *Gives all links*
`vote`: *Gives a link to vote for this FBot*
`invite`: *Gives a link to invite FBot to your server*
`Github`: *Gives a link to view FBots Github page*
`Top.gg`/`Topgg`: *Gives a link to view FBots Top.gg page*
`server`: *Gives a link to join FBots server*
`Minecraft`/`MC`: *Gives infomation to join our MC server*""",

"""**Fun Commands**

`snipe`: **NEW** *Get the last deleted message*
`bonk` `@user`/`image url`: **NEW** *BONK*
`bigpp` `@user`/`image url`: **NEW** *Who's got a big pp? You can!*
`fball`/`8ball` <question>: **NEW** *FBot will answer your most burning questions*
`say` `<message>`: *Makes FBot say whatever you want*
`dm`/`dms`: *Bring FBot into your DMs, why? Who knows!*""",

"""**Counting Commands**

`setcounter`/`counter`/`counting`: **NEW ADMIN ONLY** *Sets the current channel to the counting channel*
`number`/`last`: **NEW** *Gets the last number for counting*
`highscores`/`highscore`/`hs`: **NEW** *Gets your server and 5 servers with the highest counting highscores*""")

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
`send` `<channel_id>` `<message>`: *Sends a message to a channel*"""]

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

def setup(bot):
    bot.add_cog(cmds(bot))
