import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars()

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="commands", aliases=["cmds"])
    async def _Commands(self, ctx):
        name = ctx.author.display_name
        
        embed = discord.Embed(title="FBot Commands", description="**Write `FBot ` (the prefix) however you want, I don't care**\n"
                                                                 "*Shorthands for this command are:* `commands`/`cmds`\n"
                                                                 "\n**General Commands**\n"
                                                                 "`on`/`off`: *Toggles FBot*\n"
                                                                 "`help`/`?`: *Gives some helpful links and commands*\n"
                                                                 "`modtoggle` `on`/`off`: **ADMIN ONLY** *Allows only admin to toggle FBot*\n"
                                                                 "`prefix` `reset`/`<newprefix>`: **NEW ADMIN ONLY** *Resets or changes FBot's prefix*\n"
                                                                 "`respond` `few`/`some`/`all`: **NEW ADMIN ONLY** *Changes the amount of triggers FBot responds to*\n"
                                                                 "\n**Infomation Commands**\n"
                                                                 "`info`: *Displays some insight into the bot*\n"
                                                                 "`status`: *Displays the status of the bot in the current channel*\n"
                                                                 "`session`/`uptime`: *Gives a session overview*\n"
                                                                 "`version`/`ver`: *Shows the version of the bot*\n"
                                                                 "`ping`: *Shows the current ping for the bot*\n"
                                                                 "`events`/`event`: *Shows any events that are running and gives an overview of it*\n"
                                                                 "`notices`/`notice`: *Shows some cool stuff :)*\n"
                                                                 "`pn`/`patchnotes` `<ver>`: *Gives you the patchnotes for a version, use recent for the most recent version*\n"
                                                                 "\n**Link Commands**\n"
                                                                 "`links`: *Gives all links*\n"
                                                                 "`vote`: *Gives a link to vote for this FBot*\n"
                                                                 "`invite`: *Gives a link to invite FBot to your server*\n"
                                                                 "`Github`: *Gives a link to view FBots Github page*\n"
                                                                 "`Top.gg`/`Topgg`: *Gives a link to view FBots Top.gg page*\n"
                                                                 "`server`: *Gives a link to join FBots server*\n"
                                                                 "`Minecraft`/`MC`: *Gives infomation to join our MC server*\n"
                                                                 "\n**Fun Commands**\n"
                                                                 "`say` `<message>`: *Makes FBot say whatever you want*\n"
                                                                 "`quote`: *Quotes a random part from Mein Kampf*\n"
                                                                 "`dm`/`dms`: *Bring FBot into your DMs, why? Who knows!*", colour=0xF42F42)
        embed.set_footer(text=f"Commands requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="devcmds")
    @commands.is_owner()
    async def _DevCommands(self, ctx):
        name = ctx.author.display_name
        
        embed = discord.Embed(title="FBot Dev Commands", description="\n**General Commands**\n"
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
                                                                     "`lookup` `<server_id>`: *Gives a little overview of the server*\n"
                                                                     "`newinvite` `<server_id>`: *Creates a temporary invite for the server*\n"
                                                                     "\n**Misc**\n"
                                                                     "`presence` `<newpresence>`: *Changes FBot's presence*\n"
                                                                     "`send` `<channel_id>` `<message>`: *Sends a message to a channel*", colour=0xF42F42)
        embed.set_footer(text=f"Dev commands requested by {name} | Version v{ver}", icon_url=fboturl)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
