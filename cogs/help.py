from discord.ext import commands
from functions import predicate
from dbfn import reactionbook
import commands as cm

ehelp = ["""**Overview**
Welcome to FBot's economy! This will be your guide to FBot economy system.
Firstly the big question, how do you earn money? To earn money, or FBux,
indicated by this symbol: ' ~~f~~ ', you must work.

 Page 1: **Overview**
 Page 2: **Introduction**
 Page 3: **Working, Studying and Multipliers**
 Page 4: **Information and More**""",

"""**Introduction**
Working is fairly straight forward, every hour you can take a work shift and
earn your jobs worth of money (minus tax). Now I bet that sounds pretty neat,
but with FBot's multi trillion dollar maintenance costs, we have to keep tax
high, so tax can be anywhere between 50% and 90%, depending on how lucky you
are. And just so you don't have to worry, tax comes straight off your paycheck,
how thoughtful! You'll never have to worry about ~~us taking it~~ forgetting to pay
it again!

Now we have a wide selection of jobs, but you can't just apply for any one of
them - you're not qualified! Silly you, you need to take a degree first. Degrees
you say? Well glad you asked, see you can take a degree which will allow you to
apply for a certain job. Easy? Not so fast. You won't be able to study any old
degree, majority of degrees start of as locked but you will gain access to more
and more of them as you interact with FBot. Done? Not quite. As you study for
your degree, which operates similarly to the work function, you will accumulate
debt, why? Who knows! To think you're only studying to pay more taxes in the
future ~~something isn't quite right here~~.""",

"""**Working and Studying**
To work and study use `FBot work` and `FBot study`. But wait... There's more.
To find jobs and degrees, you can use `FBot degrees` and `FBot jobs`. Now this
is just mind blowing, BUT THERE'S MORE! You can't just study without a degree,
so to take a degree or apply for a job use `FBot apply <job>` or `FBot take`
`<degree>`. Bet you weren't expecting that. One final point. If you have a job
and want to pick a new one, or if your degree really isn't to your liking,
you can drop it no questions asked. So that's `FBot resign` for jobs, and `FBot`
`drop` for degrees. Make sure you know what you're doing, because you won't be
able to recover your progress for degrees. There, I'm done.

**Multipliers**
Doesn't practise make perfect? Yes. Same applies for FBot, the more you spam,
the more your multipliers increase, the relevant ones at least. There are three
types of multipliers, first is your personal one. This multiplier follows you
everywhere. Every time you interact with FBot, even in DMs, this multiplier will
increase. Second is your server multiplier. This will increase as people
interact with FBot in a server, the more a server uses FBot, the higher the
multiplier increases by. Last there is your job multiplier. This is specific to
each job and increases every time you successfully work. Multipliers are used
to increase the amount of money you earn. Your personal multiplier can also
help you unlock new degree which in turn gives you access to new jobs.""",

"""**Information**
Wanna see your progress as a FBoter? Use `FBot profile`. Wanna laugh at inferior
mortals? Use `FBot profile @inferior mortal`. Wanna view your multipliers?
Use `FBot mutlis`. Want me to stop? No? That's what I thought. You can use
`FBot cmds` to view a full list of available commands.

**Competitive, Store, Suggestions and More!**
It's no fun winning and not knowing it, know it. Use `FBot baltop` to view the
richest FBoters and `FBot debttop` to view the most in debt. With more to come,
stay posted.

Use your money, to get... more money. Learn how to commit tax evasion or money
laundering, or whatever else we choose to add! What better way to invest your
hard earned cash, than in more cash and future content!

VOTE FOR FBOT and get your entire salary WITHOUT TAX, use `FBot vote` to find
out more.

We are always working on new ways to improve FBot, if you have any suggestions,
or just wanna drop by for a chat, use `FBot server` to join our server.

Currently there is no way to remove debt, but since it doesn't cause you any
harm, you'll just have to learn to live with it - for now."""]

descriptions = ["Commands to get FBot spamming, check FBot's spamming, and limit FBots spamming",
"All the commands you need to start making FBux... and debt!",
"Commands to set up counting, show the last number, and highscores",
"Image processing, say command, mingames and more!",
"Snipe and purge, severinfo and more!",
"Info about FBot including links, uptime, version and more!"]

CMDS_EMOJI = "📃"
LINK_EMOJI = "🔗"

CONTENTS_EMOJI = "🔖"
SPAM_EMOJI = "💬"
ECON_EMOJI = "<:fbag:814645386957291550>"
COUNT_EMOJI = "🔢"
FUN_EMOJI = "🤪"
UTIL_EMOJI = "⚙️"
INFO_EMOJI = "❔"
emojis = [CONTENTS_EMOJI, SPAM_EMOJI, ECON_EMOJI, COUNT_EMOJI,
          FUN_EMOJI, UTIL_EMOJI, INFO_EMOJI]

class help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    def cmdembed(self, user, cmd, prefix):
        try: data = cm.commands[cmd]
        except: data = cm.devcmds[cmd]

        desc = data[9]
        # Temporary while not all commands have long descriptions
        if desc == "": desc = data[10]

        usage = data[8].replace("{prefix}", prefix)
        
        embed = self.bot.fn.embed(user, "**FBot " + cmd + data[0] + "**",
                                  desc, f"\n**Cooldown:** `{data[3]}s`",
                                  f"**Premium Cooldown:** `{data[4]}s`",
                                  "\n**Example usage:**", usage)

        cat = "Category: " + data[1] + data[2]
        embed.set_author(name=cat)

        embed.add_field(name="**Server only?**", value=data[5])
        embed.add_field(name="**Bot perms**", value=data[6])
        embed.add_field(name="**User perms**", value=data[7])

        embed.set_image(url=self.bot.fn.banner)

        return embed
        
    @commands.command(name="help")
    @commands.check(predicate)
    async def _Help(self, ctx, *command):

        prefix = "fbot"
        if str(ctx.channel.type) != "private":
            prefix = self.bot.db.Get_Prefix(ctx.guild.id)
        if prefix == "fbot": prefix = "fbot "

        command = " ".join(command).lower()
        if command == "":
            fn = self.bot.fn
            embed = fn.embed(ctx.author, "")

            embed.add_field(name=f"{CMDS_EMOJI} **__Helpful Commands__**",
            value="Good commands to get you started", inline=False)
            embed.add_field(name=f"**{prefix}on/off**",
            value="*Toggles response feature*")
            embed.add_field(name=f"**{prefix}cmds**",
            value="*Gives a list of commands*")
            embed.add_field(name=f"**{prefix}economy**",
            value="*Gives help for economy*")
            embed.add_field(name=f"**{prefix}help <command>**",
            value="*Gives some with a command*")
            embed.add_field(name="**prefix**",
            value="*Tells you the prefix for FBot on the server*")

            embed.add_field(name=f"{LINK_EMOJI} **__Helpful Links__**",
            value="Some useful links For reference", inline=False)
            embed.add_field(name="**Invite FBot**",
            value=f"*[Here!]({fn.invite} 'Custom invite link woooo')*")
            embed.add_field(name="**Our Support Server**",
            value=f"*[Here!]({fn.server} 'Custom server invite link woooo')*")
            embed.set_image(url=self.bot.fn.banner)

            await ctx.send(embed=embed)
        else:
            user = ctx.author
            for cmd in cm.commands:
                if command == cmd:
                    await ctx.send(embed=self.cmdembed(user, cmd, prefix))
                    return

            if ctx.author.id in self.bot.owner_ids:
                for cmd in cm.devcmds:
                    if command.startswith(cmd):
                        await ctx.send(embed=self.cmdembed(user, cmd, prefix))
                        return

            await ctx.send(f"No command called '{command}'")

    @commands.command(name="economy")
    @commands.check(predicate)
    async def _Economy(self, ctx):
        colour = self.bot.db.getcolour(ctx.author.id)
        book = reactionbook(self.bot, ctx, TITLE="FBot Economy")
        book.createpages(ehelp, ITEM_PER_PAGE=True)
        await book.createbook(MODE="numbers", COLOUR=colour, TIMEOUT=60)

    @commands.command(name="cmds", aliases=["commands"])
    @commands.check(predicate)
    async def _Commands(self, ctx):

        prefix = "fbot"
        if str(ctx.channel.type) != "private":
            prefix = self.bot.db.Get_Prefix(ctx.guild.id)
        if prefix == "fbot": prefix = "fbot "
        colour = self.bot.db.getcolour(ctx.author.id)
        
        embeds = [self.bot.fn.embed(ctx.author, "**__FBot commands__**")]
        embeds[0].set_image(url=self.bot.fn.banner)
        for i, category in enumerate(cm.categories):
            if category == "temp": break
            embeds[0].add_field(name=f"{emojis[i+1]} **{category}**",
            value=f"[Hover for more]({self.bot.fn.votetop} '{descriptions[i]}')")
            embed = self.bot.fn.embed(ctx.author,
            f"{emojis[i+1]} **__{category} Commands__**",
            f"*Use* `{prefix}help <command>` *to find more about a command*")
            for cmd, args, desc in cm.categories[category]:
                embed.add_field(name=f"**{prefix}{cmd}**", value=f"*{desc}*")
            embed.set_image(url=self.bot.fn.banner)
            embeds.append(embed)

        page = 0
        msg = await ctx.send(embed=embeds[page])

        for emoji in emojis:
            if emoji.startswith("<") and emoji.endswith(">"):
                emoji_id = int(emoji[1:-1].split(":")[2])
                for Emoji in self.bot.emojis:
                    if Emoji.id == emoji_id:
                        emoji = Emoji
                        break
            await msg.add_reaction(emoji)

        def check(reaction, user):
            emoji = (str(reaction.emoji) in emojis)
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
                page = emojis.index(str(reaction.emoji))
                await msg.edit(embed=embeds[page])
            except:
                embed = embeds[page]
                embed.set_footer(text=f"Commands timed out")
                try: await msg.edit(embed=embed)
                except: pass
                break

    @commands.command(name="devcmds")
    @commands.is_owner()
    @commands.check(predicate)
    async def _DevCommands(self, ctx):
        colour = self.bot.db.getcolour(ctx.author.id)
        book = reactionbook(self.bot, ctx, LINES=20)
        book.createpages(cm.devcmdlist, LINE="`%0`",
                         SUBHEADER="**__FBot Dev Commands__**\n")
        await book.createbook(MODE="numbers", COLOUR=colour)

def setup(bot):
    bot.add_cog(help(bot))