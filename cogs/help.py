from discord.ext import commands
from functions import predicate
from dbfn import reactionbook
import commands as cm

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
COUNT_EMOJI = "🔢"
FUN_EMOJI = "🤪"
UTIL_EMOJI = "⚙️"
INFO_EMOJI = "❔"
emojis = [CONTENTS_EMOJI, SPAM_EMOJI, COUNT_EMOJI,
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