import functions
from discord.ext import commands
from functions import ftime
from functions import fn

sessionstart = ftime.getstart()

class info(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="info")
    async def _Info(self, ctx):

        totalmembers = 0
        for servers in self.bot.guilds:
            if str(servers.id) != "264445053596991498":
                totalmembers += servers.member_count

        embed = fn.embed("FBot Info", "")
        embed.add_field(name="Session start", value=sessionstart)
        embed.add_field(name="Servers", value=len(self.bot.guilds) - 1)
        embed.add_field(name="Last Updated", value=fn.getinfo("lastupdated"))
        embed.add_field(name="Uptime", value=ftime.uptime())
        embed.add_field(name="Members", value=totalmembers)
        embed.add_field(name="Version", value=fn.getinfo("ver"))
        embed.set_footer(text="Created by justjude#2296 & LinesGuy#9260", icon_url=functions.fboturl)
        await ctx.send(embed=embed)

    @commands.command(name="serverinfo")
    async def _ServerInfo(self, ctx):
        name = ctx.author.display_name
        guild = ctx.guild
        
        memcount, botcount = 0, 0
        for member in guild.members:
            if not member.bot:memcount += 1
            else: botcount += 1

        created = guild.created_at
        d = created.strftime("%d")
        mo = created.strftime("%m")
        y = created.strftime("%y")
        created = f"{d}/{mo}/{y}"

        embed = fn.embed(guild.name, guild.description)
        embed.add_field(name="Members", value=memcount + botcount)
        embed.add_field(name="Users", value=memcount)
        embed.add_field(name="Bots", value=botcount)
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Language", value=guild.preferred_locale)
        embed.add_field(name="Created", value=created)
        embed.set_thumbnail(url=guild.icon_url)
        embed = fn.footer(embed, name, "Server info")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))
