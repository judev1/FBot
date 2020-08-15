import discord
from discord.ext import commands
from Functions import Functions as fn

ver, fboturl, variables = fn.Get_Vars(var1="vers")
vers = variables[0]

class FBot_Cogs(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="patchnotes", aliases=["pn"])
    async def _PatchNotes(self, ctx, *arg):
        name = ctx.author.display_name
        send = ctx.send

        try:
            arg = arg[0]
            pns = fn.Get_Patch_Notes(arg)
            
            if arg == "list":
                embed = discord.Embed(title="**Patch Note Arguments**", description=vers, colour=0xF42F42)
                embed.set_footer(text=f"Patchnotes requested by {name} | Version v{ver}", icon_url=fboturl)
                await send(embed=embed)

            elif pns != "ERROR":
                if arg == "recent":
                    arg = ver
                    
                embed = discord.Embed(title="FBot Patch Notes", colour=0xF42F42)
                embed.add_field(name=f"Patch notes for `v{arg}`", value=f"`{pns}`", inline=False)
                embed.set_footer(text=f"Patchnotes requested by {name} | Version v{ver}", icon_url=fboturl)
                await send(embed=embed)

            else:
                embed = discord.Embed(title="**Error:** `Invalid Argument`", description=f"```The argument '{arg}' was not recognised, for all arguments use 'FBot pn list'```", colour=0xF42F42)
                await send(embed=embed)

        except:
            embed = discord.Embed(title="**Error:** `No Argument`", description="```You didn't add an argument, for all arguments use 'FBot pn list'```", colour=0xF42F42)
            await send(embed=embed)

def setup(bot):
    bot.add_cog(FBot_Cogs(bot))
