# Folder: DiscordBots\FBot
#   File: FBot.py

from Functions import functions as fn
import discord, random, time

client = discord.Client()
remove = fn.remove

create = fn.create
checkname = fn.checkname
getsex = fn.getsex
createsex = fn.createsex

setfbot = fn.setfbot
getfbot = fn.getfbot

#Variables you can change
sexuality = ["gay", "straight", "definitley not straight", "I have no fucking clue", "like mostly gay", "half gay", "just a pedo", "bixsexual probaly"]
twss = ["That's big", "that's big", "Thats big", "thats big"]

#Variables you should not change
fbot = ["fbot", "Fbot",  "fBot",  "fbOt",  "fboT",  "FBot",  "FbOt",  "FboT",  "fBOt",  "fBoT",  "fbOT",  "FBOt",  "FbOT",  "fBOT",  "FBOT"]
tf = ["will", "will not"]

#When the Client connects to the server
@client.event
async def on_connect():
    name = client.user
    print("\n > Began signing into discord as {}".format(name))

#When the Client - Server connection is ready  
@client.event
async def on_ready():
    name = client.user
    server = client.guilds
    print(" > Finished signing into discord as {}\n".format(name))

    create(client)

#Message Replies
@client.event
async def on_message(message):
    #Variable setups for ease of use
    name = message.author
    name = str(name)
    name = remove(name, 0, 5)

    server = message.guild
    
    content = message.content
    startswith = content.startswith
    send = message.channel.send
    #Check for a FBot Status file
    try:
        getfbot(server)
    except:
        setfbot("on", server)

    #Get FBot Statu
    status = getfbot(server)
    status = remove(status, 0, 0)

    #Don't let FBot reply to it's self
    if message.author == client.user:
                return

    #Only lets justjude use it
    elif "fuck" in content:
        await message.delete()
        await send("That message violates the community guidelines")

    #The gay gif
    elif "https://cdn.zerotwo.dev/LICK/36dd6ed1-f77e-4dc3-9f4f-1a77abe2519b.gif" in content:
        await message.delete()

    #Toggle FBot
    elif content == "fbot1 off" or content == "Fbot1 off" or content == "FBot1 off":
        setfbot("off", server)
    elif content == "fbot1 on" or content == "Fbot1 on" or content == "FBot1 on":
        setfbot("on", server)
    elif status == "off":
        return

    #Get a random sexuality
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
        name = remove(content, 9, 0)
        
        try:
            info = checkname(name, server)
            usersex = getsex(info[0], info[1], server)
            await send("{}'s sexuality is: {}".format(info[0], usersex))
        except:
            await send("{} wasn't in the database".format(name))

    #That's what she said
    elif content in twss:
        await send("That's what she said")

    #West Viginia
    elif startswith("west virginia") or startswith("West Viginia") or startswith("West viginia"):
        await send("Mountain mama")
    elif startswith("country roads") or startswith("Country roads"):
        await send("Take me home")
        time.sleep(1)
        await send("To the place")
        time.sleep(1)
        await send("I BELONG")

    #Zero Two
    elif startswith("zt!") or startswith("Zt!"):
        await send("That's too gay for me, please kill me")

    #Gifs
    elif content == "smol pp":
        await send("https://tenor.com/view/tiny-small-little-just-alittle-guy-inch-gif-5676598")
    elif content == "micropenis":
        await send("https://tenor.com/view/girl-talks-naughty-small-dick-micropenis-gif-11854548")

    #Instant link reply
    elif startswith("https://"):
        await send("That's pretty gay ngl")

    #Coin flipper - feet style
    elif content == "feet pics" or content == "Feet pics":
        num = random.randint(0, 1)
        choice = tf[num]
        await message.channel.send("FBot says:")
        time.sleep(1)
        await message.channel.send("(Drum roll please)")
        time.sleep(3)
        await message.channel.send("Feet pics {} be granted!".format(choice))

    #Fuck FBot, Fuck me, Fuck you
    elif startswith("fuck ") or startswith("Fuck "):
        name = fn.remove(content, 5, 0)
        fbotcheck = fn.remove(name, 4, 0)
        if fbotcheck in fbot or name in fbot:
            await send("Yeah fuck me")
            time.sleep(1)
            await send("Wait no")
        elif content == "fuck you" or content == "Fuck you":
            await send("No fuck you")
        elif fbotcheck == "me":
            await send("Fuck you, fuck you {}".format(name))
        else:
            await send("Yeah fuck {}".format(name))

    #I am, I have, I will
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

    #You, Your, You are, You have
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
        await send("Yeah!")
        time.sleep(1)
        await send("Wait...")
        time.sleep(1)
        await send("Are you mocking me?")
        await send("That's my thing you know")

    #Die
    elif startswith("die ") or startswith("Die "):
        content = remove(content, 4, 0)
        await send("Yes die {}".format(content))
    elif content == "die" or content == "Die":
        await send("Die motherfucker")
        

    #Meme talk, Nice, F, Oof, Bruh, Hmm
    elif content == "nice" or content == "Nice":
        await message.channel.send("Not nice")
    elif content == "not nice" or content == "Not nice":
        await message.channel.send("Nice")

    elif content == "f" or content == "F":
        await send("F")

    elif startswith("oof") or startswith("Oof"):
        await send("Oof")

    elif startswith("bru") or startswith("Bru"):
        await send("Yeah {}?".format(content))

    elif startswith("hm"):
        await send("Hmmmm fuck you {}".format(name))
    elif startswith("Hm"):
        await send("Hmmmm fuck you {}".format(name))

#Client key - this is required to run
client.run('')
