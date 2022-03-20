from discord.ext import commands
import discord

import lib.functions as fn

class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def invite(self, ctx):
        embed = self.bot.embed(ctx.author, "Invite FBot to your server!", url=fn.links.invite)
        await ctx.send(embed=embed)

    @commands.command()
    async def server(self, ctx):
        embed = self.bot.embed(ctx.author, "Join our server, it's for support and fun!", url=fn.links.server)
        await ctx.send(embed=embed)

    @commands.command()
    async def github(self, ctx):
        embed = self.bot.embed(ctx.author, "All FBot's code is on github, give it a star!", url=fn.links.github)
        await ctx.send(embed=embed)

    @commands.command()
    async def links(self, ctx):

        embed = self.bot.embed(ctx.author, "FBot links",)

        embed.add_field(name=":closed_book: **__GENERAL LINKS__**", inline=False, value="The standard discord links for FBot")
        embed.add_field(name="Invite FBot", value=f"[Click here]({fn.links.invite})")
        embed.add_field(name="Support Server", value=f"[Click here]({fn.links.server})")

        embed.add_field(name=":green_book: **__EXTERNAL LINKS__**", inline=False, value="Other non-discord FBot affliated sites")
        embed.add_field(name="Our Patreon", value=f"[Click here]({fn.links.patreon})")
        embed.add_field(name="Our Website", value=f"[Click here]({fn.links.site})")
        embed.add_field(name="Our Github", value=f"[Click here]({fn.links.github})")

        embed.add_field(name=":blue_book: **__BOT LISTS__**", inline=False, value="All the bot lists which FBot is shown on")
        embed.add_field(name="discordbotlist.com", value=f"[Click here]({fn.links.dbl})")
        embed.add_field(name="top.gg", value=f"[Click here]({fn.links.top})")
        embed.add_field(name="listcord.gg", value=f"[Click here]({fn.links.ligg})")
        embed.add_field(name="discords.com/votes", value=f"[Click here]({fn.links.bfd})")
        embed.add_field(name="botlist.me", value=f"[Click here]({fn.links.blme})")
        embed.add_field(name="botlist.space", value=f"[Click here]({fn.links.blsp})")
        embed.add_field(name="discord-botlist.eu", value=f"[Click here]({fn.links.dbeu})")
        embed.add_field(name="discord.bots.gg", value=f"[Click here]({fn.links.dbgg})")

        await ctx.send(embed=embed)

    @commands.command()
    async def newinvite(self, ctx, guild: discord.Guild):
        try:
            invite = await guild.system_channel.create_invite(
                max_age=120 * 60, temporary=True)
        except:
            invite = "error resolving invite"
        await ctx.send(f"Created a temporary invite for `{guild}`\n"
                f"`{invite}`, will expire after 2 hours")

def setup(bot):
    bot.add_cog(Links(bot))