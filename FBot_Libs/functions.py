import datetime
import discord
import os
import random
from database import db
from discord.ext import commands

debug = False
m_start, h_start, d_start, mo_start = 0, 0, 0, 0

fboturl = "https://cdn.discordapp.com/icons/717735765936701450/b2649caffd40fae44442bec642b69efd.webp?size=1024"

voteurl = "https://top.gg/bot/711934102906994699/vote"
inviteurl = "https://discord.com/oauth2/authorize?client_id=711934102906994699&permissions=8&scope=bot"

githuburl = "https://github.com/judev1/FBot"
topggurl = "https://top.gg/bot/711934102906994699"

serverurl = "https://discord.gg/BDpXRq9"
prplhzurl = "https://discord.gg/zW2k2yK"
rhurl = "https://discord.gg/6SBBM3J"

class fn():

    # Turns on debug mode
    def debug(value):
        global debug
        debug = value

    # Removes known prefix's and suffix's from a string
    def remove(text, left_chars, right_chars):
        return text[left_chars:len(text) - right_chars]

    # Gets the bot token
    def gettoken(num):
        with open("./Info/Tokens.txt", "r") as file: data = file.readlines()
        return data[int(num)][:-1]

    # Get last updated, version and versions
    def getinfo(info):
        with open("./Info/Info.txt", "r") as file: data = file.readlines()
        if info == "lastupdated": return data[0][:-1]
        elif info == "ver": return data[1][:-1]
        else: raise NameError(f"No variable called '{info}'")

    # Gets the Notices
    def getnotices():
        with open("./Info/Notices.txt", "r") as file: data = file.readlines()
        notices = ""
        for line in data: notices += str(line)
        notices = eval(notices)
        return notices

    # Gets the Events
    def getevents():
        with open("./Info/Events.txt", "r") as file: data = file.readlines()
        events = ""
        for line in data: events += str(line)
        events = eval(events)
        return events

    # Gets all the files in FBot_Cogs
    def getcogs():
        cogs = []
        for cog in os.listdir("FBot_Cogs"):
            if os.path.isfile(os.path.join("FBot_Cogs", cog)):
                cogs.append([cog])
        return cogs

    # Gets all the patchnote versions
    def getpatchnotevers():
        vers = []
        for ver in os.listdir("Info/Patch_Notes"):
            if os.path.isfile(os.path.join("Info/Patch_Notes", ver)):
                vers.append([ver[:-4]])
        return vers

    # Gets the Pacth Notes for a version
    def getpatchnotes(ver):
        with open(f"./Info/Patch_Notes/{ver}.txt", "r") as file: data = file.readlines()
        lines = len(data)
        pn = ""
        for line in data: pn += str(line)
        pn = eval(pn)
        return pn, lines

    # Checks and gets the prefix
    def getprefix(bot, message):
        prefix = "fbot"
        if str(message.channel.type) != "private":
            prefix = db.Get_Prefix(message.guild.id)
        if prefix == "fbot":
            content = message.content
            if content[:5].lower() == "fbot ": prefix = content[:5]
            elif content[:6].lower() == "f bot ": prefix = content[:6]
            elif content[:23].lower() == "<@!711934102906994699> ":
                prefix = content[:6]
        return prefix

    # Checks the characters in a prefix
    def checkchars(prefix):
        bannedchars = ["{", "}", "(", ")", "[", "]", "'", '"', "`", "\\", "/",  "_", "-", "=", "*"]
        for char in prefix:
            for bannedchar in bannedchars:
                if bannedchar == char: return True, char
            return False, ""

    # Creates an embed
    def embed(title, info):
        return discord.Embed(title=title, description=info, colour=0xF42F42)

    # Creates an error embed
    def errorembed(error, info):
        return discord.Embed(title=f"**Error:** `{error}`",
                             description=f"```{info}```", colour=0xF42F42)

    # Default footer
    def footer(embed, name, command):
        text = f"{command} requested by {name} | Version v{fn.getinfo('ver')}"
        embed.set_footer(text=text, icon_url=fboturl)
        return embed

class book():

    # Creates pages for a book
    def createpages(content, line, **kwargs):

        page = ""
        lines = 0
        elements = 0
        
        empty = kwargs.get("empty", "ERROR: NO CONTENTS")
        subheader = kwargs.get("subheader", "")
        pages = kwargs.get("pages", [])
        elementsperpage = kwargs.get("lines", 8)
        getlines = kwargs.get("getlines", False)
        check_one = kwargs.get("check_one", None)
        check_two = kwargs.get("check_two", None)
        subcheck_one = kwargs.get("subcheck_one", None)
        subcheck_two = kwargs.get("subcheck_two", None)
        ctx = kwargs.get("ctx", "")
        bot = kwargs.get("bot", "")

        def check(items, bot, ctx):
            
            one, two = True, True
            sub_one, sub_two = True, True

            def switch(val):
                return False if val else True

            def format_check(tempcheck, items):
                try:
                    for i in range(4):
                        tempcheck = tempcheck.replace(f"%{i}", str(items[i]))
                except: pass
                return tempcheck
            
            if check_one:
                try:
                    tempcheck = format_check(check_one[0], items)
                    try: tempcheck = eval(tempcheck)
                    except: pass
                    one = True if tempcheck == check_one[1] else False
                except: one = False
                try:
                    if not check_one[2]: one = switch(one)
                except: pass

            if check_two:
                try:
                    tempcheck = format_check(check_two[0], items)
                    try: tempcheck = eval(tempcheck)
                    except: pass
                    two = True if tempcheck == check_two[1] else False
                except: two = False
                try:
                    if not check_two[2]: two = switch(two)
                except: pass

            if subcheck_one:
                try:
                    tempcheck = format_check(subcheck_one[0], items)
                    try: tempcheck = eval(tempcheck)
                    except: pass
                    sub_one = True if tempcheck == subcheck_one[1] else False
                except: sub_one = False
                try:
                    if not subcheck_one[2]: sub_one = switch(sub_one)
                except: pass

            if subcheck_two:
                try:
                    tempcheck = format_check(subcheck_two[0], items)
                    try: tempcheck = eval(tempcheck)
                    except: pass
                    sub_two = True if tempcheck == subcheck_two[1] else False
                except: sub_two = False
                try:
                    if not subcheck_two[2]: sub_two = switch(sub_two)
                except: pass

            return one and two and (sub_one or sub_two)
        
        for item in content:
            if check(item, bot, ctx):
                if lines == 0 and subheader != "": page += subheader + "\n"
                page += line + "\n"

                elements += 1
                lines += 1
                
                try:
                    for i in range(4):
                        page = page.replace(f"%{i}", str(item[i]))
                except: pass
                
                if elements == elementsperpage:
                    pages.append(page)
                    page = ""
                    elements = 0

        if lines == 0:
            if subheader != "": page = subheader + "\n"
            page += empty
            pages.append(page)
        elif elements != 0: pages.append(page)

        if getlines: return pages, lines
        return pages

    # Creates and manages a book
    async def createbook(bot, ctx, title, pages, **kwargs):

        header = kwargs.get("header", "") # String
        results = kwargs.get("results", 0) # Int
        
        pagenum = 1

        def get_results():
            results_min = (pagenum - 1) * 8 + 1
            if pagenum == len(pages): results_max = results
            else: results_max = pagenum * 8
            return f"Showing {results_min} - {results_max} results out of {results}"

        pagemax = len(pages)
        if results:
            header = get_results()
            if len(pages) == 0: pagemax = 1

        embed = discord.Embed(title=title, description=f"{header}\n\n{pages[pagenum - 1]}", colour=0xF42F42)
        embed.set_footer(text=f"Page {pagenum}/{pagemax}", icon_url=fboturl)
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡")
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡"]
    
        while True:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout = 60, check=check)
                await msg.remove_reaction(reaction, user)
                
                if str(reaction.emoji) == "⬅️":
                    pagenum -= 1
                    if pagenum < 1: pagenum = len(pages)
                        
                elif str(reaction.emoji) == "➡":
                    pagenum += 1
                    if pagenum > len(pages): pagenum = 1

                header = get_results() if results else header
                if str(reaction.emoji) == "⬅️" or str(reaction.emoji) == "➡":
                    embed = discord.Embed(title=title, description=f"{header}\n\n{pages[pagenum - 1]}", colour=0xF42F42)
                    embed.set_footer(text=f"Page {pagenum}/{len(pages)}", icon_url=fboturl)
                    await msg.edit(embed=embed)
            except:
                header = get_results() if results else header
                embed = discord.Embed(title="FBot Server Status", description=f"{header}\n\n{pages[pagenum - 1]}", colour=0xF42F42)
                embed.set_footer(text=f"Request timed out", icon_url=fboturl)
                await msg.edit(embed=embed)
                break

class ftime():

    # Returns the min, hour, day and month from a datetime object
    def get():
        time = datetime.datetime.now(tz=datetime.timezone.utc)
        m = time.strftime("%M")
        h = time.strftime("%H")
        d = time.strftime("%d")
        mo = time.strftime("%m")
        return m, h, d, mo

    # Sets the start time
    def setstart():        
        global m_start, h_start, d_start, mo_start
        m_start, h_start, d_start, mo_start = ftime.get()
        return ftime.getstart()

    # Gets the start time
    def getstart():
        return f"{h_start}:{m_start}, {d_start}-{mo_start} UTC"

    # Gets the current time
    def now():
        m, h, d, mo = ftime.get()
        return f"{h}:{m}, {d}-{mo} UTC"

    # Gets the uptime
    def uptime():
        m, h, d, mo = ftime.get()
        m_now, h_now, d_now, mo_now = int(m), int(h), int(d), int(mo)
        m, h, d, mo = int(m_start), int(h_start), int(d_start), int(mo_start)

        if mo > mo_now:
            mo_uptime = 60 - mo
            mo_uptime += mo_now
        else: mo_uptime = mo_now - mo
        
        if d > d_now:
            if mo == 2: d_uptime = 28 - d
            elif mo == 4 or mo == 6 or mo == 9 or mo == 10:
                d_uptime = 30 - d
            else: d_uptime = 31 - d
            d_uptime += d_now
            mo_uptime -= 1
        else: d_uptime = d_now - d

        if h > h_now:
            h_uptime = 24 - h
            h_uptime += h_now
            d_uptime -= 1
        else: h_uptime = h_now - h

        if m > m_now:
            m_uptime = 60 - m
            m_uptime += m_now
            h_uptime -= 1
        else: m_uptime = m_now - m
        
        ds = "s" if d_uptime != 1 else ""
        hs = "s" if h_uptime != 1 else ""
        ms = "s" if m_uptime != 1 else ""
        
        if d_uptime > 0:
            uptime = "{d_uptime} day{ds}, {h_uptime} hour{hs}"
        elif h_uptime > 0:
            uptime = f"{h_uptime} hour{hs}, {m_uptime} minute{ms}"
        else: uptime = f"{m_uptime} minute{ms}"
        return uptime
