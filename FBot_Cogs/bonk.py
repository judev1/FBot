import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from wand.image import Image
import time
import re
import os
import requests


bonk_img = Image(filename="./Info/bonk.png")
is_mention = re.compile("<@!?[0-9]{18}>")
is_img_url = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")
bonk_help = (
    "Command usage:\n"
    "Bonk a user: `fbot bonk <@user>`\n"
    "Bonk a picture: upload an image with the comment `fbot bonk`")
#    "Bonk a picture: `fbot bonk <image url>` or attach an image and use `fbot bonk`\n"
#    "Image url's must end in .jpg or .png, more formats will be supported soon(tm)")

class bonk(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bonk(self, ctx, to_bonk=None):
        await ctx.send("Ooopsie! The `bonk` command is temporarily disabled.")
        return
        
        debug = True
        if debug: print(f"\n\n{ctx.message.content}\n{ctx.message}")
        
        start_time = time.time()
        await ctx.trigger_typing()

        if (to_bonk is None and not ctx.message.attachments):
            # Nothing to bonk
            if debug: print("No-one to bonk, returning")
            await ctx.send(bonk_help)
            return
        elif (ctx.message.attachments):
            # Image is attached
            if debug: print("Attached image to bonk")
            await ctx.message.attachments[0].save("to_bonk")
            if debug: print("Image saved successfully")
        
        elif (is_img_url.match(to_bonk)):
            # Image is URL
            if debug: print("img_url to bonk, returning")
            # This is disabled because bonking a 100mb image halts FBot and makes my server cry for about 2 minutes
            await ctx.send("URL bonking is temporarily disabled, upload an image with the comment `fbot bonk` instead")
            return
        
            r = requests.get(to_bonk, allow_redirects=True)
            with open('to_bonk', 'wb') as file:
                file.write(r.content)
                
        elif (is_mention.match(to_bonk)):
            # Image is user avatar
            if debug: print("Avatar to bonk")
            converter = MemberConverter()
            member = await converter.convert(ctx, to_bonk)
            await member.avatar_url_as(format="jpg", static_format="jpg", size=512).save("to_bonk")
            if debug: print("Avatar image saved successfully")
        else:
            if debug: print("Nothing to bonk, returning")
            await ctx.send(bonk_help)
            return

        if debug: print("Bonking image")
        with Image(filename="to_bonk") as img:
            if len(img.sequence) > 1:
                await ctx.send(".gif files are currently not supported! Please annoy FBot devs to implement this.")
                return
            img.resize(511, 511)
            img.swirl(degree=-45)
            img.implode(amount=0.4)
            img.composite(bonk_img)
            img.save(filename="bonked.jpg")
        if debug: print("Image bonked, sending image")

        file = discord.File(fp="bonked.jpg")
        msg = await ctx.send("bonk: ", file=file)
        os.remove("bonked.jpg")
        os.remove("to_bonk")
        execution_time = time.time() - start_time
        if debug: print(f"Bonk done in {execution_time} seconds")
        # await msg.edit(content=f"bonk: `[took {execution_time} seconds]`")

    @bonk.error
    async def bonk_handler(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'to_bonk':
                await ctx.send("You must specify who you want to bonk!")
        else:
            print('Ignoring exception in command {}:'.format(
                ctx.command), file=sys.stderr)
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr)

            await ctx.send("`An error occurred while executing this command.`")

            
    

def setup(bot):
    bot.add_cog(bonk(bot))

"""
import urllib2
from wand.image import Image

with Image(filename="img.jpg") as img:
    img.implode(amount=-0.5)
    img.save(filename="out.jpg")

avatar
"""
