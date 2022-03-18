from discord.ext import commands
import lib.functions as fn
import lib.database as db

LARROW_EMOJI = "⬅️"
RARROW_EMOJI = "➡️"

toptypes = {
    "votes": ("votes", "anywhere", "with `{}` vote(s) this month", "with {} votes"),
    "voters": ("votes", "anywhere", "with `{}` vote(s) this month", "with {} votes"),
    "voting": ("votes", "anywhere", "with `{}` vote(s) this month", "with {} votes"),
    "counting": ("counting", "server", "with a highscore of `{}`", "with {}"),
    "counters": ("counting", "server", "with a highscore of `{}`", "with {}")
}

medals = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:"}
prefixes = {1: "st", 2: "nd", 3: "rd"}

NAME = 0
USAGE = 1
TOP = 2
RANK = 3

class Top(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def top(self, ctx, toptype):

        if toptype in toptypes:

            data = toptypes[toptype]
            obj_id = ctx.author.id

            if data[USAGE] == "server":
                obj_id = ctx.guild.id
                if str(ctx.channel.type) == "private":
                    await ctx.reply(f"Top {toptype} can only be used in a server")
                    return

            async with ctx.channel.typing():
                top, selftop, rank = db.gettop(toptype, 12, obj_id)
                embed = self.bot.embed(
                    ctx.author,
                    f"FBot Top {data[NAME]}",
                    f"Ranked `{rank}` " + data[TOP].format(selftop)
                )

                cache = self.bot.cache.names
                for rank, row in enumerate(top):

                    ID, typeitem = row
                    name = cache.get(ID)

                    if not name:
                        if data[USAGE] == "server":
                            try:
                                name = self.bot.get_guild(ID).name
                            except:
                                name = "Unknown Server"
                        else:
                            name = fn.formatname(await self.bot.fetch_user(ID))
                        cache.add(ID, name)

                    if obj_id == ID:
                        name = f"**--> __{name}__ <--**"

                    rank += 1
                    medal = ":medal:"
                    if rank in medals:
                        medal = medals[rank]

                    if int(str(rank)[-1]) in [1, 2, 3] and rank not in [11, 12, 13]:
                        rank = f"{medal} {rank}{prefixes[rank]} with "
                    else:
                        rank = f":medal: {rank}th with "

                    embed.add_field(
                        name=rank + data[RANK].format(typeitem),
                        value=name
                    )

            await ctx.send(embed=embed)

        else:
            await ctx.reply("We don't have a leaderboard for that")

def setup(bot):
    bot.add_cog(Top(bot))