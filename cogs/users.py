from discord.ext import commands
import discord

LARROW_EMOJI = "⬅️"
RARROW_EMOJI = "➡️"
toptypes = ["votes", "counting"]

class users(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    async def _Profile(self, ctx, user: discord.User=None):
        await ctx.send("This command is being reworked")

    @commands.command(name="top")
    async def _Top(self, ctx, toptype):

        if toptype in toptypes:
            if toptype == "counting":
                if str(ctx.channel.type) == "private":
                    await ctx.send(f"Top {toptype} can only be used in a server")
                    return
                obj_id = ctx.guild.id
            else:
                obj_id = ctx.author.id

            async with ctx.channel.typing():
                fn, db = self.bot.fn, self.bot.db
                top, selftop, rank = db.gettop(toptype, 12, obj_id)
                if toptype == "vote":
                    selftop = f"with `{selftop}` vote(s) this month"
                elif toptype == "counting":
                    selftop = f"with a highscore of `{selftop}`"
                embed = fn.embed(ctx.author, f"FBot Top {toptype}",
                                 f"Ranked `{rank}` " + selftop)

                cache = self.bot.cache["Names"]
                for rank, row in enumerate(top):
                    ID, typeitem = row
                    name = cache.get(ID)
                    if not name:
                        if toptype == "counting":
                            try: name = self.bot.get_guild(ID).name
                            except: name = "Unknown Server"
                            if ctx.guild.id == ID:
                                name = f"**--> __{name}__ <--**"
                        else:
                            name = fn.formatname(await self.bot.fetch_user(ID))
                            if ctx.author.id == ID:
                                name = f"**--> __{name}__ <--**"
                        cache.add(ID, name)

                    rank = str(rank + 1)
                    if rank == "1": medal = ":first_place:"
                    elif rank == "2": medal = ":second_place:"
                    elif rank =="3": medal = ":third_place:"
                    else: medal = ":medal:"

                    if rank.endswith("1") and rank != "11": rank = f"{medal} {rank}st with "
                    elif rank.endswith("2") and rank != "12": rank = f"{medal} {rank}nd with "
                    elif rank.endswith("3") and rank != "13": rank = f"{medal} {rank}rd with "
                    else: rank = f"{medal} {rank}th with "

                    if toptype == "votes": content = f"{typeitem} votes"
                    elif toptype == "counting": content = f"`{typeitem}`"
                    embed.add_field(name=rank + content, value=name)

            await ctx.send(embed=embed)

        else:
            await ctx.send("We don't have a leaderboard for that...")

def setup(bot):
    bot.add_cog(users(bot))