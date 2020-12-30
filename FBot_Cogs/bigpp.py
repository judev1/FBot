import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from wand.image import Image as wand_image
from PIL import Image as pil_image
import time
import re
import os
import sys
import requests


bigpp_img = wand_image(filename="./Info/bigpp.png")
is_mention = re.compile("<@!?[0-9]{18}>")
is_img_url = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")
bigpp_help = (
    "Command usage:\n"
    "Bigpp a user: `fbot bigpp <@user>`\n"
    "Bigpp a picture: upload an image with the comment `fbot bigpp`")
#    "Bigpp a picture: `fbot bigpp <image url>` or attach an image and use `fbot bigpp`\n"
#    "Image url's must end in .jpg or .png, more formats will be supported soon(tm)")

class bigpp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bigpp(self, ctx, to_bigpp=None):
        #await ctx.send("Ooopsie! The `bigpp command is temporarily disabled.")
        #return
        
        debug = False
        if debug: print(f"\n\n{ctx.message.content}\n{ctx.message}")
        
        start_time = time.time()
        await ctx.trigger_typing()

        if (to_bigpp is None and not ctx.message.attachments):
            # Nothing to bigpp
            if debug: print("No-one to bigpp, returning")
            await ctx.send(bigpp_help)
            return
        elif (ctx.message.attachments):
            # Image is attached
            if debug: print("Attached image to bigpp")
            await ctx.message.attachments[0].save("to_bigpp")
            if debug: print("Image saved successfully")
        
        elif (is_img_url.match(to_bigpp)):
            # Image is URL
            if debug: print("img_url to bigpp, returning")
            # This is disabled because bigpping a 100mb image halts FBot and makes my server cry for about 2 minutes
            await ctx.send("URL bigpping is temporarily disabled, upload an image with the comment `fbot bigpp` instead")
            return
        
            r = requests.get(to_bigpp, allow_redirects=True)
            with open('to_bigpp', 'wb') as file:
                file.write(r.content)
                
        elif (is_mention.match(to_bigpp)):
            # Image is user avatar
            if debug: print("Avatar to bigpp")
            converter = MemberConverter()
            member = await converter.convert(ctx, to_bigpp)
            await member.avatar_url_as(format="jpg", static_format="jpg", size=512).save("to_bigpp")
            if debug: print("Avatar image saved successfully")
        else:
            if debug: print("Nothing to bigpp, returning")
            await ctx.send(bigpp_help)
            return

        if debug: print("Bigpping image")

        with pil_image.open("to_bigpp") as img:
            resized_img = img.resize((511, 511))
            resized_img.save("resized_to_bigpp", "JPEG")
        
        with wand_image(filename="to_bigpp") as img:
            if len(img.sequence) > 1:
                await ctx.send(".gif files are currently not supported! Please annoy FBot devs to implement this.")
                return
            img.resize(511, 511)
            img.implode(amount=-7)
            img.composite(bigpp_img)
            img.save(filename="bigpped.jpg")
        if debug: print("Image bigpped, sending image")

        file = discord.File(fp="bigpped.jpg")
        msg = await ctx.send("bigpp: ", file=file)
        os.remove("bigpped.jpg")
        os.remove("to_bigpp")
        execution_time = time.time() - start_time
        if debug: print(f"bigpp done in {execution_time} seconds")

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
    bot.add_cog(bigpp(bot))

"""
import urllib2
from wand.image import Image

with Image(filename="img.jpg") as img:
    img.implode(amount=-0.5)
    img.save(filename="out.jpg")

avatar
"""
