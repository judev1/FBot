import os, time, datetime, random, discord
from discord.ext import commands
from Database import Database as db

m_start = 0
h_start = 0
d_start = 0
mo_start = 0

debug = False

fboturl = "https://images.discordapp.net/avatars/711934102906994699/6ab406f40bc3517802fd4402955da1b0.png?size=512"
hitlerurl = "https://pearlsofprofundity.files.wordpress.com/2014/05/adolf-hitler-graphic-1.jpg"

voteurl = "https://top.gg/bot/711934102906994699/vote"
inviteurl = "https://discord.com/oauth2/authorize?client_id=711934102906994699&permissions=8&scope=bot"

githuburl = "https://github.com/judev1/FBot"
topggurl = "https://top.gg/bot/711934102906994699"

serverurl = "https://discord.gg/BDpXRq9"
prplhzurl = "https://discord.gg/zW2k2yK"
rhurl = "https://discord.gg/6SBBM3J"

class Functions():

    # Turns on debug mode
    def Debug(value):
        global debug
        debug = value

    # Removes known prefix's and suffix's from a string
    def Remove(text, left_chars, right_chars):
        return text[left_chars:len(text) - right_chars]

    # Sets up and checks files for severs
    def Setup():
        newpath = r".servers"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            os.popen('attrib +h ' + newpath)
            print(" > Created a folder to store server data")

    # Gets the bot token
    def Get_Token(num):
        file = open("./Info/Tokens.txt", "r")
        data = file.readlines()
        file.close()
        return Functions.Remove(data[int(num)], 0, 1)

    # Gets the Notices
    def Get_Notices():
        file = open("./Info/Notices.txt", "r")
        data = file.readlines()
        file.close()
        notices = ""
        for lines in data:
            notices += str(lines)
        notices = eval(notice)
        return notices

    # Gets the Events
    def Get_Events():
        file = open("./Info/Events.txt", "r")
        data = file.readlines()
        file.close()
        event = ""
        for lines in data:
            events += str(lines)
        events = eval(events)
        return events

    # Get last updated, version and versions
    def Get_Info(info):
        file = open("./Info/Info.txt", "r")
        data = file.readlines()
        file.close()
        if info == "lastupdated":
            return Functions.Remove(data[0], 0, 1)
        elif info == "ver":
            return Functions.Remove(data[1], 0, 1)
        elif info == "vers":
            return Functions.Remove(data[2], 0, 1)
        else:
            raise NameError(f"No variable called '{info}'")

    # Checks and gets the prefix
    def Get_Prefix(bot, message):
        prefix = "fbot"
        if str(message.channel.type) != "private":
            prefix = db.Get_Prefix(message.guild.id)
        if prefix == "fbot":
            content = message.content
            if content[:5].lower() == "fbot ":
                prefix = content[:5]
            elif content[:6].lower() == "f bot ":
                prefix = content[:6]
            elif content[:23].lower() == "<@!711934102906994699> ":
                prefix = content[:6]
        return prefix

    # Gets the Pacth Notes for a version
    def Get_Patch_Notes(ver):
        try:
            if ver == "recent":
                ver = Functions.Get_Info("ver")
            file = open(f"./Info/Patch_Notes/{ver}.txt", "r")
            data = file.readlines()
            file.close()
            pns = ""
            for lines in data:
                pns += str(lines)
            pns = eval(pns)
            return pns
        except:
            if ver == "recent" or ver == Functions.Get_Info("ver"):
                return "Currently there are no patchnotes for this version"
            else:
                return "ERROR"

    # Gets requested variables
    def Get_Vars(**kwargs):
        variables = []
        for args in kwargs:
            arg = kwargs[args]
            if arg == "hitlerurl":
                variables.append(hitlerurl)
            elif arg == "voteurl":
                variables.append(voteurl)
            elif arg == "inviteurl":
                variables.append(inviteurl)
            elif arg == "githuburl":
                variables.append(githuburl)
            elif arg == "topggurl":
                variables.append(topggurl)
            elif arg == "serverurl":
                variables.append(serverurl)
            elif arg == "prplhzurl":
                variables.append(prplhzurl)
            elif arg == "rhurl":
                variables.append(rhurl)
            elif arg == "serverlogs":
                variables.append(serverlogs)
            elif arg == "creators":
                variables.append(creators)
            elif arg == "lastupdated":
                variables.append(Functions.Get_Info("lastupdated"))
            elif arg == "vers":
                variables.append(Functions.Get_Info("vers"))
            else:
                raise NameError(f"No variable called '{arg}'")
        return Functions.Get_Info("ver"), fboturl, variables

    # Checks the characters in a prefix
    def Check_Chars(prefix):
        bannedchars = ["{", "}", "(", ")", "[", "]", "'", '"', "`", "\\", "/",  "_", "-", "=", "*"]
        for char in prefix:
            for bannedchar in bannedchars:
                if bannedchar == char:
                    return True, char
            return False, ""

    # That's what she said
    def TWSS(message):
        twords1 = ["penis", "dick", "cock", "pussy", "vagina", "boobs", "tits"]
        twords2 = ["harder", "deeper", "louder", "insert", "penetrate", "inside", "daddy", "ass", "finger", "cum", "suck", "flaccid", "tight", "shaft", "grows", "enlargens", "extends", "finish", "horny", "thirsty"]
        twords3 = ["big", "huge", "long", "faster", "fast", "further", "gentle", "gently", "slow", "quick", "push", "small", "wet", "blow", "ball", "thick", "hard", "fat", "sweaty", "hold", "love", "like"]
        triggerwords = [twords1, twords2, twords3]
        
        score = 0
        for triggers in twords1:
            if triggers in message:
               score += 25
        for triggers in twords2:
            if triggers in message:
               score += 15
        for triggers in twords3:
            if triggers in message:
               score += 10

        if score >= 25:
            return True
        return False




class Book():

    # Creates pages for a book
    def Create_Pages(array, line, **kwargs):

        page = ""
        lines = 0
        elements = 0
        
        empty = kwargs.get("empty", "Arrogant piece of shit you thought this wouldn't be empty") # String used on empty page
        subheader = kwargs.get("subheader", "") # String
        pages = kwargs.get("pages", []) # A list of pages
        getlines = kwargs.get("getlines", False) # Boolean
        check_one = kwargs.get("check_one", "") # Tuple (Integer, String) or Tuple (Function, String)
        check_two = kwargs.get("check_two", "")
        subcheck_one = kwargs.get("subcheck_one", "") # Tuple (Integer, String) or Tuple (Function, String)
        subcheck_two = kwargs.get("subcheck_two", "")
        ctx = kwargs.get("ctx", "") # Context from the Discord event
        bot = kwargs.get("bot", "") # Bot data from Discord

        def check(items, bot, ctx):
            
            one = True
            two = True
            sub_one = True
            sub_two = True

            def switch(val):
                return False if val else True

            def format_check(tempcheck, items):
                try:
                    tempcheck = tempcheck.replace("%0", str(items[0]))
                    tempcheck = tempcheck.replace("%1", str(items[1]))
                    tempcheck = tempcheck.replace("%2", str(items[2]))
                    tempcheck = tempcheck.replace("%3", str(items[3]))
                except:
                    pass
                return tempcheck
            
            if check_one != "":
                try:
                    one = True if items[check_one[0]] == check_one[1] else False
                except:
                    tempcheck = format_check(check_one[0], items)
                    tempcheck = eval(tempcheck)
                    one = True if {tempcheck} == check_one[1] else False
                try:
                    if not check_one[2]:
                        one = switch(one)
                except:
                    pass

            if check_two != "":
                try:
                    two = True if items[check_two[0]] != check_two[1] else False
                except:
                    tempcheck = format_check(check_two[0], items)
                    tempcheck = eval(tempcheck)
                    two = True if {tempcheck} == check_two[1] else False
                try:
                    if not check_two[2]:
                        two = switch(two)
                except:
                    pass

            if subcheck_one != "":
                try:
                    sub_one = True if items[subcheck_one[0]] == subcheck_one[1] else False
                        
                except:
                    tempcheck = format_check(subcheck_one[0], items)
                    tempcheck = eval(tempcheck)
                    sub_one = True if {tempcheck} == subcheck_one[1] else False
                try:
                    if not subcheck_one[2]:
                        sub_one = switch(sub_one)
                except:
                    pass

            if subcheck_two != "":
                try:
                    sub_two = True if items[subcheck_two[0]]== subcheck_two[1] else False
                except:
                    tempcheck = format_check(subcheck_two[0], items)
                    tempcheck = eval(tempcheck)
                    sub_two = True if tempcheck == subcheck_two[1] else False
                try:
                    if not subcheck_two[2]:
                        sub_two = switch(sub_two)
                except:
                    pass

            return one and two and (sub_one or sub_two)
        
        for items in array:
            if check(items, bot, ctx):
                if lines == 0 and subheader != "":
                    page += subheader + "\n"
                page += line + "\n"

                elements += 1
                lines += 1
                
                try:
                    page = page.replace("%0", str(items[0]))
                    page = page.replace("%1", str(items[1]))
                    page = page.replace("%2", str(items[2]))
                    page = page.replace("%3", str(items[3]))
                except:
                    pass
                
                if elements == 8:
                    pages.append(page)
                    page = ""
                    elements = 0

        if lines == 0:
            if subheader != "":
                page = subheader + "\n"
            page += empty
            pages.append(page)
        elif elements != 0:
            pages.append(page)

        if getlines:
            return pages, lines
        return pages

    # Creates and manages a book
    async def Create_Book(bot, ctx, title, pages, **kwargs):

        header = kwargs.get("header", "") # String
        results = kwargs.get("results", 0) # Int
        
        pagenum = 1

        def get_results():
            results_min = (pagenum - 1) * 8 + 1
            if pagenum == len(pages):
                results_max = results
            else:
                results_max = pagenum * 8
            return f"Showing {results_min} - {results_max} results out of {results}"

        pagemax = len(pages)
        if results:
            header = get_results()
            if len(pages) == 0:
                pagemax = 1

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
                    if pagenum < 1:
                        pagenum = len(pages)
                        
                elif str(reaction.emoji) == "➡":
                    pagenum += 1
                    if pagenum > len(pages):
                        pagenum = 1

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




class Time():

    # Sets the start time
    def Set_Start():
        timenow = datetime.datetime.now()
        
        global m_start, h_start, d_start, mo_start
        m_start = timenow.strftime("%M")
        h_start = timenow.strftime("%H")
        d_start = timenow.strftime("%d")
        mo_start = timenow.strftime("%m")

    # Gets the start time
    def Get_Start():
        return "{}:{}, {}.{} BST".format(h_start, m_start, d_start, mo_start)

    # Gets the current time
    def Now():
        timenow = datetime.datetime.now()
        m_now = timenow.strftime("%M")
        h_now = timenow.strftime("%H")
        d_now = timenow.strftime("%d")
        mo_now = timenow.strftime("%m")
        return "{}:{}, {}.{} BST".format(h_now, m_now, d_now, mo_now)

    # Gets the uptime
    def Uptime():

        now = datetime.datetime.now()
        m_now = int(now.strftime("%M"))
        h_now = int(now.strftime("%H"))
        d_now = int(now.strftime("%d"))
        mo_now = int(now.strftime("%m"))

        m = int(m_start)
        h = int(h_start)
        d = int(d_start)
        mo = int(mo_start)

        if mo > mo_now:
            mo_uptime = 60 - mo
            mo_uptime += mo_now
        else:
            mo_uptime = mo_now - mo
        
        if d > d_now:
            if mo == 2:
                d_uptime = 28 - d
            elif mo == 4 or mo == 6 or mo == 9 or mo == 10:
                d_uptime = 30 - d
            else:
                d_uptime = 31 - d
            d_uptime += d_now
            mo_uptime -= 1
        else:
            d_uptime = d_now - d

        if h > h_now:
            h_uptime = 24 - h
            h_uptime += h_now
            d_uptime -= 1
        else:
            h_uptime = h_now - h

        if m > m_now:
            m_uptime = 60 - m
            m_uptime += m_now
            h_uptime -= 1
        else:
            m_uptime = m_now - m

        ds = ""
        hs = ""
        ms = ""
        uptime = ""
        
        if d_uptime != 1:
            ds = "s"
        if h_uptime != 1:
            hs = "s"
        if m_uptime != 1:
            ms = "s"
        
        if d_uptime > 0:
            uptime = "{} day{}, {} hour{}".format(d_uptime, ds, h_uptime, hs)

        elif h_uptime > 0:
            uptime = "{} hour{}, {} minute{}".format(h_uptime, hs, m_uptime, ms)

        else:
            uptime = "{} minute{}".format(m_uptime, ms)

        return uptime
