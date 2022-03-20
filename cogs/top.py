from discord.ext import commands

import lib.functions as fn
import lib.database as db

LARROW_EMOJI = "⬅️"
RARROW_EMOJI = "➡️"

toptypes = {
    "voters": ("votes", "anywhere", "with `{}` vote(s) this month", "with {} votes"),
    "voting": ("votes", "anywhere", "with `{}` vote(s) this month", "with {} votes"),
    "votes": ("votes", "anywhere", "with `{}` vote(s) this month", "with {} votes"),
    "counters": ("counting", "server", "with a highscore of `{}`", "with {}"),
    "counting": ("counting", "server", "with a highscore of `{}`", "with {}")
}

medals = {1: ":first_place:", 2: ":second_place:", 3: ":third_place:"}
suffixes = {1: "st", 2: "nd", 3: "rd"}

def suffix(rank):
    if int(str(rank)[-1]) in [1, 2, 3] and rank not in [11, 12, 13]:
        return f"{rank}{suffixes[rank]}"
    else:
        rank = f"{rank}th"

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
                obj_id = -1
                if str(ctx.channel.type) != "private":
                    obj_id = ctx.guild.id

            async with ctx.channel.typing():
                top, score, rank = db.gettop(data[NAME], 12, obj_id)
                embed = self.bot.embed(
                    ctx.author,
                    f"FBot Top {data[NAME]}",
                )
                if obj_id != -1:
                    embed.description = f"Ranked `{suffix(rank)}` {data[TOP].format(score)}"

                cache = self.bot.cache.names
                for rank, row in enumerate(top):

                    ID, score = row
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

                    if len(name) > 20:
                        name = name[:18] + "..."

                    if obj_id == ID:
                        name = f"**__{name}__**"

                    rank += 1
                    medal = ":medal:"
                    if rank in medals:
                        medal = medals[rank]

                    rank = f"{medal} {suffix(rank)}"

                    embed.add_field(
                        name=f"{rank} {data[RANK].format(score)}",
                        value=name
                    )

            await ctx.send(embed=embed)

        else:
            await ctx.reply("We don't have a leaderboard for that")

def setup(bot):
    bot.add_cog(Top(bot))