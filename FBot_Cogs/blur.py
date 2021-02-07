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


is_mention = re.compile("<@!?[0-9]{18}>")
is_img_url = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")
blur_help = (
    "Command usage:\n"
    "Blur a user: `fbot blur <@user>`\n"
    "Blur a user 50%: `fbot blur <@user> 50`\n"
    "Blur a picture: upload an image with the comment `fbot blur`\n"
    "Blur a picture 75%: upload an image with the comment `fbot blur 75`\n"
    "Default blur amount is 25%")

class blur(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, type=commands.BucketType.user)
    async def blur(self, ctx, to_blur=None, amount=25):
        await ctx.trigger_typing()

        if (to_blur is None and not ctx.message.attachments):
            # Nothing to blur
            await ctx.send(blur_help)
            return
        elif (ctx.message.attachments):
            # Image is attached
            await ctx.message.attachments[0].save("to_blur")
                
        elif (is_mention.match(to_blur)):
            # Image is user avatar
            converter = MemberConverter()
            member = await converter.convert(ctx, to_blur)
            await member.avatar_url_as(format="jpg", static_format="jpg", size=512).save("to_blur")
        else:
            await ctx.send(blur_help)
            return

        with wand_image(filename="to_blur") as img:
            if len(img.sequence) > 1:
                await ctx.send(".gif files are currently not supported! Please annoy FBot devs to implement this.")
                return
            angle = amount * 5 / 9 # convert percent to degrees (100% = 180 degrees)
            img.rotational_blur(angle=angle)
            img.save(filename="blurred.jpg")

        file = discord.File(fp="blurred.jpg")
        msg = await ctx.send("blur: ", file=file)
        os.remove("blurred.jpg")
        os.remove("to_blur")      

def setup(bot):
    bot.add_cog(blur(bot))
