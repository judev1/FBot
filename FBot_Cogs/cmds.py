from discord.ext import commands
from functions import book
from functions import fn

class cmds(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="commands", aliases=["cmds"])
    async def _Commands(self, ctx, *page):
        name = ctx.author.display_name
        
        page0 = ("**Write `FBot ` (the prefix) however you want, I don't care**\n"
                 "*If you ever lose your prefix use plain* `prefix` *to get it*\n"
                 "*Shorthands for this command are:* `commands`/`cmds`\n\n"
                 
                 " Page 1: **General Commands**\n"
                 " Page 2: **Infomation Commands**\n"
                 " Page 3: **Link Commands**\n"
                 " Page 4: **Fun Commands**\n"
                 " Page 5: **Counting Commands**",)

        page1 = ("`on`/`off`: *Toggles FBot*\n"
                 "`help`/`?`: *Gives some helpful links and commands*\n"
                 "`modtoggle` `on`/`off`: **ADMIN ONLY** *Allows only admin to toggle FBot*\n"
                 "`prefix` `reset`/`<newprefix>`: **ADMIN ONLY** *Resets or changes FBot's prefix*\n"
                 "`status` `server`: *Gives an overview of the status for the server*\n"
                 "`status` `server` `mod`: **ADMIN ONLY** *Displays the status for hidden channels too*\n"
                 "`respond` `few`/`some`/`all`: **ADMIN ONLY** *Changes the amount of triggers FBot responds to*\n"
                 "`purge`/`thanos` `<number>`: **NEW ADMIN ONLY** Deletes the last number of messages",)

        page2 = ("`info`: *Displays some infomation about the FBot*\n"
                 "`serverinfo`: *Displays infomation about the server*"
                 "`status`: *Displays the status of the bot in the current channel*\n"
                 "`session`/`uptime`: *Gives a session overview*\n"
                 "`version`/`ver`: *Shows the version of the bot*\n"
                 "`ping`: *Shows the current ping for the bot*\n"
                 "`events`/`event`: *Shows any events that are running and gives an overview of it*\n"
                 "`notices`/`notice`: *Shows some cool stuff :)*\n"
                 "`pn`/`pns`/`patchnotes` (`<ver>`/`list`/`recent`): *Gives you the patchnotes for a version*",)

        page3 = ("`links`: *Gives all links*\n"
                 "`vote`: *Gives a link to vote for this FBot*\n"
                 "`invite`: *Gives a link to invite FBot to your server*\n"
                 "`Github`: *Gives a link to view FBots Github page*\n"
                 "`Top.gg`/`Topgg`: *Gives a link to view FBots Top.gg page*\n"
                 "`server`: *Gives a link to join FBots server*\n"
                 "`Minecraft`/`MC`: *Gives infomation to join our MC server*",)

        page4 = ("`snipe`: **NEW** *Get the last deleted message*\n"
                 "`bonk` `@user`/`image url`: **NEW** *BONK*\n"
                 "`bigpp` `@user`/`image url`: **NEW** *Who's got a big pp? You can!*\n"
                 "`fball`/`8ball` <question>: **NEW** *FBot will answer your most burning questions*"
                 "`say` `<message>`: *Makes FBot say whatever you want*\n"
                 "`dm`/`dms`: *Bring FBot into your DMs, why? Who knows!*",)

        page5 = ("`setcounter`/`counter`/`counting`: **NEW ADMIN ONLY** *Sets the current channel to the counting channel*\n"
                 "`number`/`last`: **NEW** *Gets the last number for counting*\n"
                 "`highscores`/`highscore`/`hs`: **NEW** *Gets your server and 5 servers with the highest counting highscores*",)

        commandpages = (page0, page1, page2, page3, page4, page5)

        pages = book.createpages((page0,), "%0")
        pages = book.createpages((page1,), "%0", subheader="**General Commands**", pages=pages)
        pages = book.createpages((page2,), "%0", subheader="**Infomation Commands**", pages=pages)
        pages = book.createpages((page3,), "%0", subheader="**Link Commands**", pages=pages)
        pages = book.createpages((page4,), "%0", subheader="**Fun Commands**", pages=pages)
        pages = book.createpages((page5,), "%0", subheader="**Counting Commands**", pages=pages)
        await book.createbook(self.bot, ctx, "FBot Commands", pages)

    @commands.command(name="devcmds")
    @commands.is_owner()
    async def _DevCommands(self, ctx):
        name = ctx.author.display_name
        
        embed = fn.embed(

"FBot Dev Commands",

"\n**General Commands**\n"
"`devon`/`devoff`: *Toggles FBot*\n"
"`devmodtoggle` `on`/`off`: *Allows only admin to toggle FBot*\n"
"`treload`: *Reloads Trigger.csv*\n"
"`eval` `<to eval>`: *Evaluates content*\n"

"\n**Cog Commands**\n"
"`reload` `<cog>`: *Reloads a cog*\n"
"`load` `<cog>`: *Loads a cog*\n"
"`unload` `<cog>`: *Unloads a cog*\n"

"\n**Server Commands**\n"
"`servers`/`members`: *Gives a neat little overview of all the servers FBot is in*\n"
"`search` `<query>`: *Searches for a server name*\n"
"`lookup` `<server_id>`: *Gives an overview of a server*\n"
"`newinvite` `<server_id>`: *Creates a temporary invite for the server*\n"

"\n**Misc**\n"
"`presence` `<newpresence>`: *Changes FBot's presence*\n"
"`send` `<channel_id>` `<message>`: *Sends a message to a channel*"

)

        embed = fn.footer(embed, name, "Dev commands")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(cmds(bot))
