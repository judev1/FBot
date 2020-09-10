import discord
from discord.ext import commands
from discord.ext.commands import MemberConverter
from wand.image import Image
import time
import re
import os
import requests


bonk_img = Image(filename="./FBot_Libs/bonk.png")
#is_mention = re.compile("<@![0-9]{18}>")
is_img_url = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")
bonk_help = (
    "Command usage:\n"
    "Bonk a user: `fbot bonk <@user>`\n"
    "Bonk a picture: `fbot bonk <image url>` or attach an image and use `fbot bonk`\n"
    "Image url's must end in .jpg or .png, more formats will be supported soon(tm)")

class BonkCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bonk(self, ctx, to_bonk=None):
        start_time = time.time()
        await ctx.trigger_typing()

        if (to_bonk is None and not ctx.message.attachments):
            # Nothing to bonk
            await ctx.send(bonk_help)
            return
        elif (ctx.message.attachments):
            # Image is attached
            await ctx.message.attachments[0].save("to_bonk")
        
        elif (is_img_url.match(to_bonk)):
            # Image is linked
            r = requests.get(to_bonk, allow_redirects=True)
            with open('to_bonk', 'wb') as file:
                file.write(r.content)
        #elif (is_mention.match(to_bonk.strip())):
        elif (ctx.message.mentions):
            # Image is user avatar
            converter = MemberConverter()
            member = await converter.convert(ctx, to_bonk)
            await member.avatar_url_as(format="jpg", static_format="jpg", size=512).save("to_bonk")
        else:
            await ctx.send(bonk_help)
            return
        
        with Image(filename="to_bonk") as img:
            if len(img.sequence) > 1:
                await ctx.send(".gif files are currently not supported! Please annoy FBot devs to implement this.")
                return
            img.resize(511, 511)
            img.swirl(degree=-45)
            img.implode(amount=0.4)
            img.composite(bonk_img)
            img.save(filename="bonked.jpg")

        file = discord.File(fp="bonked.jpg")
        msg = await ctx.send("bonk: ", file=file)
        os.remove("bonked.jpg")
        os.remove("to_bonk")
        execution_time = time.time() - start_time
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
    bot.add_cog(BonkCog(bot))

"""
import urllib2
from wand.image import Image

with Image(filename="img.jpg") as img:
    img.implode(amount=-0.5)
    img.save(filename="out.jpg")

avatar
"""
