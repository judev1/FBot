# Folder: DiscordBots\FBot
#   File: FBot.py

#FEATURES TO BE ADDED AT SOME POINT:
#BYE, IKR, BRO, WTF, HEY, FUCKING, DANG IT, DUMBASS, SUCK

from Functions import functions as fn
import discord, random, time, os, datetime

client = discord.Client()
remove = fn.remove

create = fn.create
setup = fn.setup

ping = fn.ping

checkname = fn.checkname
getsex = fn.getsex
createsex = fn.createsex

setfbot = fn.setfbot
getfbot = fn.getfbot

fbotin = fn.fbotin
fbotcmd = fn.fbotcmd


#Variables you can change
sexuality = ["gay", "straight", "definitley not straight", "I have no fucking clue", "like mostly gay", "half gay", "just a pedo", "bixsexual probaly"]
twss = ["That's big", "that's big", "Thats big", "thats big"]
banned = []

#Variables you should not change
fbot = ["fbot", "Fbot",  "fBot",  "fbOt",  "fboT",  "FBot",  "FbOt",  "FboT",  "fBOt",  "fBoT",  "fbOT",  "FBOt",  "FbOT",  "fBOT",  "FBOT", "<@711934102906994699>"]
tf = ["will", "will not"]

fboturl = "https://images.discordapp.net/avatars/711934102906994699/6ab406f40bc3517802fd4402955da1b0.png?size=512"

creator = "justjude#2296"
ver = "1.5"
lastupdated = "11.06.20"

sessionstart = datetime.datetime.now()
h = sessionstart.strftime("%H")
m = sessionstart.strftime("%M")
d = sessionstart.strftime("%d")
mo = sessionstart.strftime("%m")
y = sessionstart.strftime("%y")
sessionstart = "{}:{}, {}.{}.{}".format(h, m, d, mo, y)

#When the Client connects to the server
@client.event
async def on_connect():
    
    name = client.user
    print("\n > Began signing into discord as {}".format(name))


#When the Server connection is ready  
@client.event
async def on_ready():
    
    name = client.user
    print(" > Finished signing into discord as {}\n".format(name))
        
    create(client)
    create(client)

#When the Client joins a Guild
@client.event
async def on_guild_join():

    create(client)
    create(client)

#Message Replies
@client.event
async def on_message(message):

    #Variable setups for ease of use
    name = message.author
    name = str(name)
    name = remove(name, 0, 5)

    content = message.content
    startswith = content.startswith
    endswith = content.endswith
    send = message.channel.send

    server = message.guild
    channel = message.channel

    setup(server, channel)
    data = setup(server, channel)
    
    server = data[0]
    channel = data[1]
    
    #Check for a FBot's Status file
    try:
        getfbot(server, channel)
    except:
        setfbot("off", server, channel)


    #Get FBot's Status
    status = getfbot(server, channel)
    status = remove(status, 0, 0)
    
    #Don't let FBot reply to its self
    if message.author == client.user:
        return

    #Prevents USER from sending any messages or interacting with FBot
    #elif name == "USER":
        #return
        #await message.delete()
        #await send("You violate the community guidelines")

    #Prevents members who are not USER from sending any messages
    #elif name != "USER":
        #return
        #await message.delete()
        #await send("You violate the community guidelines")

    #Checks if phrase is banned
    #elif banned in content:
        #await message.delete()
        #await send("{}, your message violates the community guidelines")

    #FBot Help
    elif fbotcmd(content, "help") or fbotcmd(content, "?"):
        embed = discord.Embed(title="FBot Help", description="**Use `fbot on/off` to toggle fbot**\n\n"
                                                             "**Use `fbot cmd` for a list of commands**\n\n"
                                                             "**For more infomation go to:**\n"
                                                             "[*My Github*](https://github.com/judev1/FBot), "
                                                             "[*My top.gg*](https://top.gg/bot/711934102906994699), or "
                                                             "[*Contact Me!*](https://discord.gg/BDpXRq9)\n\n"
                                                             "**You can help FBot too!**\n"
                                                             "[Vote here!](https://top.gg/bot/711934102906994699/vote)", colour=0xF42F42)
        embed.set_footer(text="Help requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)

    #FBot Info
    elif fbotcmd(content, "info"):
        totalmembers = 0
        for servers in client.guilds:
            totalmembers += servers.member_count
        embed = discord.Embed(title="TOTAL SERVER COUNT: `{}`\n"
                                    "TOTAL MEMBER COUNT: `{}`\n"
                                    "LAST UPDATED: `{}`\n"
                                    "SESSION START: `{}`\n"
                                    "VERSION: `v{}`\n"
                                    "PING: `{}ms`".format(len(client.guilds), totalmembers, lastupdated, sessionstart, ver, ping(message.created_at)), colour=0xF42F42)
        embed.set_footer(text="Info requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)
    

    #FBot Notice Board
    elif fbotcmd(content, "nb") or fbotcmd(content, "noticeboard") or fbotcmd(content, "notice board"):
        embed = discord.Embed(title="FBot Notice Board", description="**We are currently holding an event!**\n"
                                                                     "*Use* `FBot events` *or* [*visit FBot's Server for more info*](https://discord.gg/BDpXRq9)\n\n", colour=0xF42F42)
        embed.set_footer(text="Nb requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)

    #FBot Events
    elif fbotcmd(content, "events") or fbotcmd(content, "event"):
        embed = discord.Embed(title="FBot Events", description="**We are currently holding an event!**\n"
                                                               "We are creating an about page for FBot and we would like your help!\n"
                                                               "[*Visit FBot's Server for more info*](https://discord.gg/BDpXRq9)", colour=0xF42F42)
        embed.set_footer(text="Events requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)

    #FBot Vote
    elif fbotcmd(content, "vote"):
        embed = discord.Embed(title="FBot Vote", description="[Vote for fbot here!](https://top.gg/bot/711934102906994699/vote)", colour=0xF42F42)
        embed.set_footer(text="Vote requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)

    #FBot Status
    elif fbotcmd(content, "status"):
        embed = discord.Embed(title="FBot is currently set to `{}` in this channel".format(status), colour=0xF42F42)
        embed.set_footer(text="Status requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)

    #FBot Ping
    elif fbotcmd(content, "ping"):
        embed = discord.Embed(title="The ping is `{}ms`".format(ping(message.created_at)), colour=0xF42F42)
        embed.set_footer(text="Ping requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)

    #FBot Commands
    elif fbotcmd(content, "commands") or fbotcmd(content, "command") or fbotcmd(content, "cmd") or fbotcmd(content, "cmds"):
        embed = discord.Embed(title="FBot Commands", description="**Write `FBot ` (the prefix) however you want, I don't care**\n"
                                                                 "*Shorthands for this command are:* `commands`/`command`/`cmds`/`cmd`\n\n"
                                                                 "`on`/`off`: *Toggles FBot*\n"
                                                                 "`help`/`?`: *Gives some helpful links and commands*\n"
                                                                 "`info`: *Displays some insight into the bot*\n"
                                                                 "`nb`/`noticeboard`/`notice board`: *Shows some cool stuff :)*\n"
                                                                 "`events`/`event`: *Shows any events that are running and gives an overview of it*\n"
                                                                 "`vote`: *Gives a link to vote for this bot*\n"
                                                                 "`status`: *Displays the status of the bot in the current channel*\n"
                                                                 "`ping`: *Shows the current ping for the bot*\n".format(status), colour=0xF42F42)
        embed.set_footer(text="Commands requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await message.channel.send(embed=embed)
    
    #Toggle FBot
    elif fbotcmd(content, "off"):
        setfbot("off", server, channel)
    elif fbotcmd(content, "on"):
        setfbot("on", server, channel)
    elif status == "off":
        return

    #Get a random sexuality for yourself (new one for each server)
    elif content == "gayscale" or content == "Gayscale":
        num = len(sexuality) - 1
        num = random.randint(0, num)
        usersex = sexuality[num]
        
        info = checkname(name, server)
        
        if info[0] == name:
            usersex = getsex(info[0], info[1], server)
        else:
            createsex(name, usersex, server)
        await send("{} your sexuality is: {}".format(name, usersex))

    #Get someone's gayscale
    elif startswith("gayscale ") or startswith("Gayscale "):
        username = name
        name = remove(content, 9, 0)
        
        try:
            info = checkname(name, server)
            usersex = getsex(info[0], info[1], server)
            await send("{}'s sexuality is: {}".format(info[0], usersex))
        except:
            await send("{} wasn't in the database".format(name))

    #Built-in gifs
    elif content == "smol pp" or content == "Smol pp":
        await send("https://tenor.com/view/tiny-small-little-just-alittle-guy-inch-gif-5676598")
    elif content == "micropenis" or content == "Micropenis":
        await send("https://tenor.com/view/girl-talks-naughty-small-dick-micropenis-gif-11854548")

    #Instant link reply
    elif startswith("https://"):
        await send("That's pretty gay ngl")

    #Coin flipper - feet style
    elif content == "feet pics" or content == "Feet pics":
        num = random.randint(0, 1)
        choice = tf[num]
        await message.channel.send("FBot says:")
        time.sleep(0.5)
        await message.channel.send("(Drum roll please)")
        time.sleep(2)
        await message.channel.send("Feet pics {} be granted!".format(choice))

    #That's what she said
    elif content in twss:
        await send("That's what she said")

    #West Viginia
    elif startswith("country roads") or startswith("Country roads"):
        await send("Take me home")
    elif startswith("to the place") or startswith("To the place"):
        await send("I BELONG")
    elif startswith("west virginia") or startswith("West Viginia") or startswith("West viginia"):
        await send("Mountain mama")
    elif startswith("take me home") or startswith("Take me home"):
        await send("Country roads")

    #Fuck FBot, Fuck me, Fuck you, Fuck
    elif startswith("fuck ") or startswith("Fuck ") or startswith("f ") or startswith("f "):
        name = fn.remove(content, 5, 0)
        fbotcheck = fn.remove(name, 4, 0)
        if fbotin(fbotcheck) or fbotin(name):
            await send("Yeah fuck me")
            time.sleep(1)
            await send("Wait no")
        elif content == "fuck you" or content == "Fuck you" or content == "fuck u" or content == "Fuck u":
            await send("No fuck you")
        elif content == "f you" or content == "F you" or content == "f u" or content == "F u" or content == "fu" or content == "Fu":
            await send("No fuck you")
        elif content == "fuck me" or content == "Fuck me":
            await send("Oh yes, fuck me, fuck me hard daddy")
        elif content == "f me" or content == "F me":
            await send("Oh yes, fuck me, fuck me hard daddy")
        elif content == "fuck me " or content == "Fuck me ":
            await send("Oh yes, fuck you {}".format(name))
        elif content == "f me " or content == "F me ":
            await send("Oh yes, fuck you {}".format(name))
        else:
            await send("Yeah fuck {}".format(name))
    elif content == "fuck" or content == "Fuck":
        await send("FUCK!")
    
    #Call on FBot
    elif startswith("fbot ") or startswith("Fbot ") or startswith("FBot "):
        content = remove(content, 5, 0)
        await send("No {} {}".format(name, content))
    elif startswith("fbots ") or startswith("Fbots ") or startswith("FBots "):
        content = remove(content, 5, 0)
        await send("No {}'s {}".format(name, content))
    elif startswith("fbot's ") or startswith("Fbot's ") or startswith("FBot's "):
        content = remove(content, 5, 0)
        await send("No {}'s {}".format(name, content))
    elif fbotin(content):
        await send("Yes {}...?".format(name))

    #I am, I have, I will, I would
    elif startswith("im ") or startswith("Im "):
        content = fn.remove(content, 3, 0)
        await send("Yeah {}'s {}".format(name, content))
    elif startswith("i'm ") or startswith("I'm "):
        content = fn.remove(content, 4, 0)
        await send("Yeah {}'s {}".format(name, content))
    elif startswith("i am ") or startswith("I am "):
        content = fn.remove(content, 5, 0)
        await send("Yeah {}'s {}".format(name, content))

    elif startswith("ive ") or startswith("Ive "):
        content = fn.remove(content, 4, 0)
        await send("Yeah {} has {}".format(name, content))
    elif startswith("i've ") or startswith("I've "):
        content = fn.remove(content, 5, 0)
        await send("Yeah {} has {}".format(name, content))
    elif startswith("i have ") or startswith("I have "):
        content = fn.remove(content, 7, 0)
        await send("Yeah {} has {}".format(name, content))

    elif startswith("ill ") or startswith("Ill "):
        content = fn.remove(content, 4, 0)
        await send("Yeah {} will {}".format(name, content))
    elif startswith("i'll ") or startswith("I'll "):
        content = fn.remove(content, 5, 0)
        await send("Yeah {} will {}".format(name, content))
    elif startswith("i will ") or startswith("I will "):
        content = fn.remove(content, 7, 0)
        await send("Yeah {} will {}".format(name, content))
    
    elif startswith("id ") or startswith("Id "):
        content = fn.remove(content, 3, 0)
        await send("Yeah {} would {}".format(name, content))
    elif startswith("i'd ") or startswith("I'd "):
        content = fn.remove(content, 4, 0)
        await send("Yeah {} would {}".format(name, content))
    elif startswith("i would ") or startswith("I would "):
        content = fn.remove(content, 8, 0)
        await send("Yeah {} would {}".format(name, content))

    #You, Your, You are, You have
    elif startswith("u ") or startswith("U "):
        content = fn.remove(content, 2, 0)
        await send("Yeah you {}".format(content))
    elif startswith("ur ") or startswith("Ur "):
        content = fn.remove(content, 3, 0)
        await send("Yeah your {}".format(content))
    elif startswith("you ") or startswith("You "):
        content = fn.remove(content, 4, 0)
        await send("Yeah you {}".format(content))
    elif startswith("your ") or startswith("Your "):
        content = fn.remove(content, 5, 0)
        await send("Yeah your {}".format(content))
        
    elif startswith("youre ") or startswith("Youre "):
        content = fn.remove(content, 6, 0)
        await send("Yeah you're {}".format(content))
    elif startswith("you're ") or startswith("You're "):
        content = fn.remove(content, 7, 0)
        await send("Yeah you're {}".format(content))
        
    elif startswith("youve ") or startswith("Youve "):
        content = fn.remove(content, 5, 0)
        await send("Yeah you have {}".format(content))
    elif startswith("you've ") or startswith("You've "):
        content = fn.remove(content, 6, 0)
        await send("Yeah you have {}".format(content))

    #It, It is, It will
    elif startswith("it ") or startswith("It "):
        content = fn.remove(content, 3, 0)
        await send("Yeah it {}".format(content))
        
    elif startswith("its ") or startswith("Its "):
        content = fn.remove(content, 4, 0)
        await send("Yeah its {}".format(content))
    elif startswith("it's ") or startswith("It's "):
        content = fn.remove(content, 5, 0)
        await send("Yeah it's {}".format(content))

    elif startswith("itll ") or startswith("Itll "):
        content = fn.remove(content, 5, 0)
        await send("Yeah it will {}".format(content))
    elif startswith("it'll ") or startswith("It'll "):
        content = fn.remove(content, 6, 0)
        await send("Yeah it will {}".format(content))

    #This, There, That, That is
    elif startswith("this ") or startswith("This "):
        content = fn.remove(content, 5, 0)
        await send("Yeah this {}".format(content))

    elif startswith("there ") or startswith("There "):
        content = fn.remove(content, 6, 0)
        await send("Yeah there {}".format(content))

    elif startswith("that ") or startswith("That "):
        content = fn.remove(content, 5, 0)
        await send("Yeah that {}".format(content))
    elif startswith("thats ") or startswith("Thats "):
        content = fn.remove(content, 6, 0)
        await send("Yeah that's {}".format(content))
    elif startswith("that's ") or startswith("That's "):
        content = fn.remove(content, 7, 0)
        await send("Yeah that's {}".format(content))

    #Let us
    elif startswith("let ") or startswith("Let "):
        content = fn.remove(content, 4, 0)
        await send("Yeah let {}".format(content))
    elif startswith("lets ") or startswith("Lets "):
        content = fn.remove(content, 5, 0)
        await send("Yeah let's {}".format(content))
    elif startswith("let's ") or startswith("Let's "):
        content = fn.remove(content, 6, 0)
        await send("Yeah let's {}".format(content))

    #Who, What, When, Where, Why and How
    elif startswith("Who ") or startswith("Who "):
        content = fn.remove(content, 4, 0)
        await send("a building")
    elif startswith("whos ") or startswith("Whos "):
        content = fn.remove(content, 5, 0)
        await send("a building")
    elif startswith("Who's ") or startswith("Who's "):
        content = fn.remove(content, 6, 0)
        await send("a building")
        
    elif startswith("what ") or startswith("What "):
        content = fn.remove(content, 5, 0)
        await send("a building")
    elif startswith("whats ") or startswith("Whats "):
        content = fn.remove(content, 6, 0)
        await send("a building")
    elif startswith("what's ") or startswith("What's "):
        content = fn.remove(content, 7, 0)
        await send("a building")
        
    elif startswith("when ") or startswith("When "):
        content = fn.remove(content, 5, 0)
        await send("a building")
    elif startswith("whens ") or startswith("Whens "):
        content = fn.remove(content, 6, 0)
        await send("a building")
    elif startswith("When's ") or startswith("When's "):
        content = fn.remove(content, 7, 0)
        await send("a building")
        
    elif startswith("where ") or startswith("Where "):
        content = fn.remove(content, 6, 0)
        await send("a building")
    elif startswith("wheres ") or startswith("Wheres "):
        content = fn.remove(content, 7, 0)
        await send("a building")
    elif startswith("where's ") or startswith("Where's "):
        content = fn.remove(content, 8, 0)
        await send("a building")
        
    elif startswith("why ") or startswith("Why "):
        content = fn.remove(content, 4, 0)
        await send("a building")
    elif startswith("whys ") or startswith("Whys "):
        content = fn.remove(content, 5, 0)
        await send("a building")
    elif startswith("why's ") or startswith("Why's "):
        content = fn.remove(content, 6, 0)
        await send("a building")
        
    elif startswith("how ") or startswith("How "):
        content = fn.remove(content, 4, 0)
        await send("a building")
    elif startswith("hows ") or startswith("Hows "):
        content = fn.remove(content, 5, 0)
        await send("a building")
    elif startswith("how's ") or startswith("How's "):
        content = fn.remove(content, 6, 0)
        await send("a building")

    #Yes and No
    elif startswith("yes"):
        await send("No")
    elif startswith("Yes"):
        await send("No")
    elif startswith("YES"):
        await send("NO")

    elif content == "no" or startswith("noo"):
        await send("Yes")
    elif content == "No" or startswith("Noo"):
        await send("Yes")
    elif content == "NO" or startswith("NOO"):
        await send("YES")

    #Yeah - Are you mocking me?
    elif startswith("yeah") or startswith("Yeah"):
        await send("Yeah! Sounds good {}".format(name))      

    #Meme talk: Nice, No you, Cool, Die, Lol, Lmao, Lmfao, Stfu, F, Oof, Bruh, Hmm, Ree
    elif content == "nice" or content == "Nice":
        await send("Not nice")
    elif content == "not nice" or content == "Not nice":
        await send("Nice")

    elif content == "no u" or content == "No u" or content == "no you" or content == "No you":
        await send("No you")

    elif content == "cool" or content == "Cool":
        await send("Not cool")
    elif startswith("cooo") or startswith("Cooo"):
        await send("Not {}".format(content))

    elif content == "lol" or content == "Lol" or content == "LOL":
        await send("No actually, not funny")
    elif content == "lmao" or content == "Lmao" or content == "LMAO":
        await send("No actually, not funny")
    elif content == "lfmao" or content == "Lmfao" or content == "LMFAO":
        await send("No actually, not funny")

    elif startswith("stfu ") or startswith("Stfu "):
        content = remove(content, 5, 0)
        await send("No, {}, *you* shut the fuck up".format(content))
    elif content == "stfu" or content == "Stfu":
        await send("No *you* shut the fuck up")

    elif startswith("die ") or startswith("Die "):
        content = remove(content, 4, 0)
        await send("Yes die {}".format(content))
    elif content == "die" or content == "Die":
        await send("Die motherfucker")
        
    elif content == "f" or content == "F":
        await send("F")

    elif (startswith("oo") or startswith("Oo")) and endswith("o"):
        content = remove(content, 1, 0)
        await send("No, not o{}".format(content))
    elif startswith("OO") and content.endswith("O"):
        content = remove(content, 1, 0)
        await send("No, not O{}".format(content))

    elif (startswith("oo") or startswith("Oo")) and endswith("f"):
        await send("Oof")
    
    elif startswith("bru") or startswith("Bru"):
        content = remove(content, 1, 0)
        await send("Yeah b{}?".format(content))

    elif startswith("hm") or startswith("Hm"):
        content = remove(content, 1, 0)
        await send("H{} fuck you {}".format(content, name))

    elif startswith("ree") or startswith("Ree"):
        content = remove(content, 1, 0)
        await send("R{}".format(content))

    #Haha and Hehe
    elif (startswith("he") or startswith("He") or startswith("HE")) and (endswith("he") or endswith("HE")):
        content = remove(content, 1, 0)
        await send("H{}, you sound pathetic, fuck you".format(content))
    elif (startswith("ha") or startswith("Ha") or startswith("HA")) and (endswith("ha") or endswith("HA")):
        content = remove(content, 1, 0)
        await send("H{}, you sound pathetic, fuck you".format(content))
        
    elif (startswith("eh") or startswith("Eh") or startswith("EH")) and (endswith("he") or endswith("HE")):
        content = remove(content, 1, 0)
        await send("E{}, you sound pathetic, fuck you".format(content))
    elif (startswith("ah") or startswith("Ah") or startswith("AH")) and (endswith("ha") or endswith("HA")):
        content = remove(content, 1, 0)
        await send("A{}, you sound pathetic, fuck you".format(content))

    elif (startswith("he") or startswith("He") or startswith("HE")) and (endswith("eh") or endswith("EH")):
        content = remove(content, 1, 0)
        await send("H{}, you sound pathetic, fuck you".format(content))
    elif (startswith("ha") or startswith("Ha") or startswith("HA")) and (endswith("ah") or endswith("AH")):
        content = remove(content, 1, 0)
        await send("H{}, you sound pathetic, fuck you".format(content))
        
    elif (startswith("eh") or startswith("Eh") or startswith("EH")) and (endswith("eh") or endswith("EH")):
        content = remove(content, 1, 0)
        await send("E{}, you sound pathetic, fuck you".format(content))
    elif (startswith("ah") or startswith("Ah") or startswith("AH")) and (endswith("ah") or endswith("AH")):
        content = remove(content, 1, 0)
        await send("A{}, you sound pathetic, fuck you".format(content))

    #Thanks, Thank you, Tysm
    elif content == "thanks" or content == "Thanks" or content == "thank you" or content == "Thank you" or content == "ty" or content == "Ty":
        await send("Actually no thank you")
    elif startswith("thanks ") or startswith("Thanks ") or startswith("thank you ") or startswith("Thank you ") or startswith("ty ") or startswith("Ty "):
        await send("No, just no, they didn't do anything")
    elif content == "tysm" or content == "Tysm":
        await send("That's a stupid thing to be *so* thankful for")

    #Hello, Hi and Welcome
    elif content == "hello" or content == "Hello" or content == "hi" or content == "Hi":
        await send("SHUT UP, NO ONE CARES")
    elif startswith("hello ") or startswith("Hello ") or startswith("hi ") or startswith("Hi "):
        await send("WHY DONT I GET A HELLO!?")
    elif startswith("welcome ") or startswith("Welcome ") or startswith("WELCOME "):
        content = remove(content, 8, 0)
        await send("Welcome {}".format(content))
    elif startswith("welcome") or startswith("Welcome") or startswith("WELCOME"):
        await send("WELCOME!")

    #Smiley faces
    elif startswith(":(") or content == "D:":
        await send("Be happy bitch")
    elif startswith(":)") or content == ":D":
        await send("Wish I could be happy, but I'm just a bot")
    elif startswith("<3") or content == ":3":
        await send("Cute.")
    elif content == ":O" or content == ":0" or content == ":o":
        time.sleep(1)
        await send("What the-")
        time.sleep(1)
        await send("Bad time?")
    elif content == ":|":
        await send("Seriously?")


#Client key - this is required to run
client.run('')
#Testing FBot - a seperate client key I have for testing only
#client.run('')
