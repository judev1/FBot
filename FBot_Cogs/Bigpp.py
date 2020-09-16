import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from wand.image import Image
import time
import re
import os
import requests


big_pp = Image(filename="./FBot_Libs/bigpp.png")
#is_mention = re.compile("<@![0-9]{18}>")
is_img_url = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")
bigpp_help = (
    "Command usage:\n"
    "Bigpp a user: `fbot bigpp <@user>`\n"
    "Bigpp a picture: `fbot bigpp <image url>` or attach an image and use `fbot bigpp`\n"
    "Image url's must end in .jpg or .png, more formats will be supported soon(tm)")

class BigppCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bigpp(self, ctx, to_bigpp=None):
        start_time = time.time()
        await ctx.trigger_typing()

        if (to_bigpp is None and not ctx.message.attachments):
            # Nothing to bigpp
            await ctx.send(bigpp_help)
            return
        elif (ctx.message.attachments):
            # Image is attached
            await ctx.message.attachments[0].save("to_bigpp")
        
        elif (is_img_url.match(to_bigpp)):
            # Image is linked
            r = requests.get(to_bigpp, allow_redirects=True)
            with open('to_bigpp', 'wb') as file:
                file.write(r.content)
        #elif (is_mention.match(to_bigpp.strip())):
        elif (ctx.message.mentions):
            # Image is user avatar
            converter = MemberConverter()
            member = await converter.convert(ctx, to_bigpp)
            await member.avatar_url_as(format="jpg", static_format="jpg", size=512).save("to_bigpp")
        else:
            await ctx.send(bigpp_help)
            return
        
        with Image(filename="to_bigpp") as img:
            if len(img.sequence) > 1:
                await ctx.send(".gif files are currently not supported! Please annoy FBot devs to implement this.")
                return
            img.resize(511, 511)
            img.implode(amount=-7)
            img.composite(big_pp)
            img.save(filename="bigpped.jpg")

        file = discord.File(fp="bigpped.jpg")
        msg = await ctx.send("bigpp: ", file=file)
        os.remove("bigpped.jpg")
        os.remove("to_bigpp")
        execution_time = time.time() - start_time
        # await msg.edit(content=f"bigpp: `[took {execution_time} seconds]`")

    @bigpp.error
    async def bigpp_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'to_bigpp':
                await ctx.send("You must specify who you want to bigpp!")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

            await ctx.send("`An error occurred while executing this command.`")

            
    

def setup(bot):
    bot.add_cog(BigppCog(bot))

"""
import urllib2
from wand.image import Image

with Image(filename="img.jpg") as img:
    img.implode(amount=-0.5)
    img.save(filename="out.jpg")

avatar
"""
