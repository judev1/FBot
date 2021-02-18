from discord.ext import commands
from functions import cooldown

class info(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="info")
    @commands.check(cooldown)
    async def _Info(self, ctx):

        ftime = self.bot.ftime
        fn = self.bot.fn

        totalmembers = 0
        for servers in self.bot.guilds:
            totalmembers += servers.member_count

        embed = self.bot.fn.embed(ctx.author, "FBot Info")
        embed.add_field(name="Session start", value=ftime.start)
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name="Last Updated", value=fn.getinfo("lastupdated"))
        embed.add_field(name="Uptime", value=ftime.uptime())
        embed.add_field(name="Members", value=totalmembers)
        embed.add_field(name="Version", value=fn.getinfo("ver"))
        await ctx.send(embed=embed)

    @commands.command(name="servinfo")
    @commands.guild_only()
    @commands.check(cooldown)
    async def _ServInfo(self, ctx):
        guild = ctx.guild

        memcount = guild.member_count
        #memcount, botcount = 0, 0
        #for member in guild.members:
        #    if not member.bot:memcount += 1
        #    else: botcount += 1

        created = guild.created_at
        d = created.strftime("%d")
        mo = created.strftime("%m")
        y = created.strftime("%y")
        created = f"{d}/{mo}/{y}"

        embed = self.bot.fn.embed(ctx.author, guild.name) # guild.description
        embed.add_field(name="Members", value=memcount)# + botcount)
        #embed.add_field(name="Users", value=memcount)
        #embed.add_field(name="Bots", value=botcount)
        embed.add_field(name="Voice channels", value=len(guild.voice_channels))
        embed.add_field(name="Text channels", value=len(guild.text_channels))
        embed.add_field(name="Roles", value=len(guild.roles))
        #embed.add_field(name="Owner", value=guild.owner)
        embed.add_field(name="Language", value=guild.preferred_locale)
        embed.add_field(name="Created", value=created)
        embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="premium")
    @commands.check(cooldown)
    async def _Premium(self, ctx):
        await ctx.send("https://fbot.breadhub.uk/premium")

def setup(bot):
    bot.add_cog(info(bot))
