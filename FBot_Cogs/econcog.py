from discord.ext import commands
from functions import predicate
import economy as e
import discord

LARROW_EMOJI = "⬅️"
RARROW_EMOJI = "➡️"
toptypes = ["votes", "vote", "counting", "multi", "servmulti", "multis", "servmultis", "fbux", "bal", "netbal", "netfbux", "debt"]

class fakeuser: id = 0
user = fakeuser()

def formatname(name, ID):
    if not name:
        name = "Deleted User"
    else:
        name = name.name.replace("*", "")
        name = name.replace("`", "")
        name = name.replace("_", "")
        name = name.replace("||", "")
        #name = f"<@!{ID}> ({name})"
    return name

class economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    @commands.check(predicate)
    async def _Profile(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum
        profile = list(db.getprofile(user.id))
        job = profile[4]
        if profile[5] == "None":
            degree = "No degree"
        else:
            degree = profile[5]
            degree = f"{degree} - {profile[6]}/{e.courses[degree][0]}"
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s profile:")
        embed.add_field(name="FBux", value=fnum(profile[0]))
        embed.add_field(name="Debt", value=fnum(profile[2]))
        embed.add_field(name="Job", value=job)
        embed.add_field(name="Net FBux", value=fnum(profile[1]))
        embed.add_field(name="Net Debt", value=fnum(profile[3]))
        embed.add_field(name="Degree", value=degree)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="gift")
    @commands.is_owner()
    @commands.check(predicate)
    async def _Gift(self, ctx, amount, user: discord.User=None):
        if not user: user = ctx.author
        self.bot.db.updatebal(user.id, amount)
        await ctx.send("Lucky you")        

    @commands.command(name="scheme")
    @commands.check(predicate)
    async def _Scheme(self, tx):
        db = self.bot.db
        user = ctx.author
        
    @commands.command(name="bal")
    @commands.check(predicate)
    async def _Balance(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db, fnum = self.bot.db, self.bot.fn.fnum
        bal, debt = db.getbal(user.id)
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s balance",
                f"FBux: {fnum(bal)}", f"Debt: {fnum(debt)}")
        await ctx.send(embed=embed)

    @commands.command(name="multis")
    @commands.check(predicate)
    async def _Multipliers(self, ctx, user: discord.User=None):
        if not user: user = ctx.author
        db = self.bot.db
        job = db.getjob(user.id)
        if job == "Unemployed":
            jobmulti = 1.0
        else: jobmulti = db.getjobmulti(user.id)
        if str(ctx.channel.type) == "private":
            multi = db.getusermulti(user.id)
            message = f"Personal Multiplier: `x{multi}`"
        else:
            multis = db.getmultis(user.id, ctx.guild.id)
            message = (f"Personal Multiplier: `x{multis[0]}`\n"
                       f"Server Multiplier: `x{multis[1]}`")
        embed = self.bot.fn.embed(ctx.author, f"{user.display_name}'s multipliers:",
                message + f"\n{job} Multiplier: `x{jobmulti}`")
        await ctx.send(embed=embed)

    @commands.command(name="inv")
    @commands.check(predicate)
    async def _Inventory(self, ctx):
        def key(x): return inv[x], x
        fn, db = self.bot.fn, self.bot.db
        inv = db.getinventory(ctx.author.id)
        sortedinv = sorted(inv, key=key)
        embeds = [fn.embed(ctx.author, f"{ctx.author.name}'s inventory")]
        for item in sortedinv:
            if len(embeds[-1].fields) == 6:
                embeds.append(fn.embed(ctx.author, f"{ctx.author.name}'s inventory"))
            data = e.items[item]
            embeds[-1].add_field(name=f"{data[2]} {data[0]} `{item}`",
                value=f"Value: {fn.fnum(data[3])} Owned: **{inv[item]}**")
        if not len(embeds[0].fields):
            embeds[-1].description = "Looks like your inventory is empty!"        

        if len(embeds) == 1:
            await ctx.send(embed=embeds[0])
            return

        page = 0
        embeds[page].set_footer(text=f"Page {page+1}/{len(embeds)}")
        msg = await ctx.send(embed=embeds[page])

        await msg.add_reaction(LARROW_EMOJI)
        await msg.add_reaction(RARROW_EMOJI)

        def check(reaction, user):
            emoji = (str(reaction.emoji) in [LARROW_EMOJI, RARROW_EMOJI])
            author = (user == ctx.author)
            message = (reaction.message.id == msg.id)
            return emoji and author and message

        wait = self.bot.wait_for
        async def forreaction():
            return await wait("reaction_add", timeout=60, check=check)
        
        while True:
            try:
                reaction, user = await forreaction()
                try: await msg.remove_reaction(reaction, user)
                except: pass
                if reaction.emoji == LARROW_EMOJI:
                    page -= 1
                    if page == -1:
                        page += len(embeds)
                elif reaction.emoji == RARROW_EMOJI:
                    page += 1
                    if page == len(embeds):
                        page -= len(embeds)
                embeds[page].set_footer(text=f"Page {page+1}/{len(embeds)}")
                await msg.edit(embed=embeds[page])
            except:
                embed = embeds[page]
                embed.set_footer(text=f"Inventory timed out")
                try: await msg.edit(embed=embed)
                except: pass
                break
    
    @commands.command(name="top")
    @commands.check(predicate)
    async def _Top(self, ctx, toptype):
        toptype = toptype.lower()
        if toptype in toptypes:
            if toptype in ["counting", "servmulti", "servmultis"]:
                if str(ctx.channel.type) == "private":
                    await ctx.send(f"top {toptype} can only be used in a server")
                    return
                obj_id = ctx.guild.id
            else: obj_id = ctx.author.id
            async with ctx.channel.typing():
                db, fn = self.bot.db, self.bot.fn
                top, selftop, rank = db.gettop(toptype, 12, obj_id)
                if toptype in ["vote", "votes"]:
                    selftop = f"with `{selftop}` vote(s) this month"
                elif toptype == "counting":
                    selftop = f"with a highscore of `{selftop}`"
                elif toptype in ["multi", "multis"]:
                    selftop = f"with a multiplier of `x{selftop/10000}`"
                elif toptype in ["servmulti", "servmultis"]:
                    selftop = f"with a server multiplier of `x{selftop/1000000}`"
                else:
                    selftop = f"with {fn.fnum(selftop)}"
                embed = fn.embed(ctx.author, f"FBot Top {toptype}",
                                 f"Ranked `{rank}` " + selftop)
                for rank, row in top:
                    ID, typeitem = row
                    if toptype in ["counting", "servmulti", "servmultis"]:
                        try: name = self.bot.get_guild(ID).name
                        except: name = "Deleted Server"
                        if ctx.guild.id == ID:
                            name = f"**--> __{name}__ <--**"
                    else:
                        name = await self.bot.fetch_user(ID)
                        name = formatname(name, ID)
                        if ctx.author.id == ID:
                            name = f"**--> __{name}__ <--**"

                    if rank == 0: rank = ":first_place: 1st with "
                    elif rank == 1: rank = ":second_place: 2nd with "
                    elif rank == 2: rank = ":third_place: 3rd with "
                    else: rank = f":medal: {rank+1}th with "

                    if toptype in ["vote", "votes"]:
                        embed.add_field(name=rank + f"{typeitem} votes", value=name)
                    elif toptype == "counting":
                        embed.add_field(name=rank + f"`{typeitem}`", value=name)
                    elif toptype in ["multi", "multis"]:
                        embed.add_field(name=rank + f"`x{typeitem/10000}`", value=name)
                    elif toptype in ["servmulti", "servmultis"]:
                        embed.add_field(name=rank + f"`x{typeitem/1000000}`", value=name)
                    else:
                        embed.add_field(name=rank + fn.fnum(typeitem), value=name)
            await ctx.send(embed=embed)
        else:
            await ctx.send("We don't have a leaderboard for that...")
            return

    @commands.command(name="item")
    @commands.check(predicate)
    async def _Item(self, ctx, item):
        item = item.lower()
        if item in e.items:
            fn = self.bot.fn
            data = e.items[item]
            owned = self.bot.db.getitem(ctx.author.id, item)
            embed = fn.embed(ctx.author,
                    f"{data[2]} **{data[0]}** (`{item}`)", f"*{data[5]}*\n")
            embed.add_field(name="Owned", value=owned)
            embed.add_field(name="Value", value=fn.fnum(data[3], bold=False))
            embed.add_field(name="Usage",
                            value=f"This item {data[6]}", inline=True)
            embed.set_author(name=f"{data[4]}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("That item doesn't exist")
    
def setup(bot):
    bot.add_cog(economy(bot))
