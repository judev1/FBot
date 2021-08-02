from discord.ext import commands
import lib.database as db
import random
import string
import json

with open("./data/colours.json", "r") as file:
    colours = json.load(file)
with open("./data/customcolours.json", "r") as file:
    customcolours = json.load(file)

for colour in customcolours:
    colours[colour] = customcolours[colour]

colour_names = list(colours)
hex_values = list(colours.values())
colour_values = dict()
for colour, value in zip(colour_names, hex_values):
    colour_values[value] = colour

class Premium(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setname(self, ctx, *, title):

        if len(title) > 50:
            await ctx.reply("Please keep your name under 50 characters")
        else:
            db.changetitle(ctx.author.id, title)
            emoji = self.bot.get_emoji(ctx.author.id)
            await ctx.message.add_reaction(emoji)
            await ctx.reply(f"It has been done, {title}")

    async def lookup(self, ctx, colour):

        colour = colour.lower()

        if colour.startswith("#"):
            colour = colour[1:]
            if len(colour) != 6:
                await ctx.reply("Hex strings can only be 6 characters long")
                return None

            hex_digits = set(string.hexdigits)
            if not all(char in hex_digits for char in colour):
                await ctx.reply("That isn't a valid hex string")
                return None

        elif len(colour.split()) == 3 and all([value.isdigit() for value in colour.split()]):

            values = [int(value) for value in colour.split()]

            if not all(value >= 0 and value <= 255 for value in values):
                await ctx.reply("RBG values must be between 0 and 255")
                return None

            colour = ""
            for value in values:
                hex_value = hex(value)[2:]
                if len(hex_value) != 2:
                    hex_value = "0" + hex_value
                colour += hex_value

        elif colour.isdigit():
            colour = int(colour)

            if colour < 0:
                await ctx.reply("Colour decimals cannot be smaller than `0`")
                return None

            if colour > 16777215:
                await ctx.reply("Colour decimals cannot be larger than `16777215`")
                return None

            colour = hex(colour)[2:]
            while len(colour) != 6:
                colour = "0" + colour

        else:

            if colour not in colours:
                await ctx.reply("That's not a supported colour name")
                return None

            colour = colours[colour]

        return colour

    @commands.command(aliases=["setcolor"])
    async def setcolour(self, ctx, *, colour):

        colour = await self.lookup(ctx, colour)
        if not colour:
            return
        colour = int(colour, 16)

        user = ctx.author
        db.changecolour(user.id, colour)
        embed = self.bot.embed(user, "Colour successfully set!")
        await ctx.send(embed=embed)
        await ctx.invoke(self.bot.get_command("colour"))

    @commands.command(aliases=["color"])
    async def colour(self, ctx, *colour):

        if colour:
            colour = " ".join(colour)
            hex_value = await self.lookup(ctx, colour)
            if not hex_value:
                return
            colour_provided = True
        else:
            colour_provided = False
            den_value = self.bot.get_colour(ctx.author.id)
            hex_value = hex(den_value)[2:]
            while len(hex_value) != 6:
                hex_value = "0" + hex_value

        if hex_value in hex_values:
            colour_name = colour_values[hex_value]
            colour = f"`#{hex_value}`,\nIt's called {colour_name}!"
        else:
            colour = f"`#{hex_value}`"

        if colour_provided:
            desc = f"That colour is {colour}"
        elif self.bot.command_invoked(ctx.message, commands=["setcolour"]):
            desc = f"{ctx.author.mention}'s updated to {colour}"
        else:
            desc = f"{ctx.author.mention}'s colour is {colour}"

        colour_trio = list()
        while len(colour_trio) != 3:
           colour = random.choice(colour_names)
           if colour not in colour_trio:
               colour = f"[{colour}](https://www.colorhexa.com/{colours[colour]})"
               colour_trio.append(colour)
        colour_trio = ", ".join(colour_trio)

        embed = self.bot.embed(ctx.author, "Colour info", desc)
        embed.add_field(name="Here are three random colours you could try:", value=colour_trio, inline=False)
        embed.set_image(url=f"https://www.singlecolorimage.com/get/{hex_value}/270x135")
        await ctx.send(embed=embed)

    @commands.command()
    async def setemoji(self, ctx):
        ping = (self.bot.latency * 100000) // 100
        embed = self.bot.embed(ctx.author, f"FBots Ping: `{ping}ms`")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Premium(bot))