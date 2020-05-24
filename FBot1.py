# Folder: DiscordBots\FBot
#   File: FBot.py

from Functions import functions as fn
import discord, random, time, os

client = discord.Client()
remove = fn.remove

create = fn.create
checkserver = fn.checkserverid
getserver = fn.getserverid
createserver = fn.createserverid
checkchannel = fn.checkchannelid
getchannel = fn.getchannelid
createchannel = fn.createchannelid


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
    print(" > Finished signing into discord as {}\n".format(name))
        
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
    send = message.channel.send

    server = message.guild
    channel = message.channel

    #Check for the Server's data
    serverid = str(server.id)
    info = checkserver(serverid)
            
    if info[0] == serverid:
        server = getserver(info[0], info[1])
    else:
        createserver(serverid, info[1])
        server = getserver(info[0], info[1])

    #Create a file for the Channel
    try:
        file = open("Servers\{}\Channel_Names.txt".format(server), "r")
        file.close()
        
    except:
        file = open("Servers\{}\Channel_Names.txt".format(server), "w+")
        file.close()  
            
    #Check for the Channel's data
    channelid = str(channel.id)
    info = checkchannel(channelid, server)
            
    if info[0] == channelid:
        channel = getchannel(info[0], info[1], server)
    else:
        createchannel(channelid, info[1], server)
        channel = getchannel(info[0], info[1], server)

    #Create a folder for the Channel
    newpath = r"Servers\{}\{}".format(server, channel)
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    
    #Check for a FBot's Status file
    try:
        getfbot(server, channel)
    except:
        setfbot("on", server, channel)


    #Get FBot's Status
    status = getfbot(server, channel)
    status = remove(status, 0, 0)

    #Don't let FBot reply to it's self
    if message.author == client.user:
                return

    #Prevents USER from sending any messages
    #elif name == "USER":
        #await message.delete()
        #await send("You violate the community guidelines")

    #Prevents members who are not MR. USER from sending any messages
    #elif name != "MR. USER":
        #await message.delete()
        #await send("You violate the community guidelines")

    #The gay gif
    elif "https://cdn.zerotwo.dev/LICK/36dd6ed1-f77e-4dc3-9f4f-1a77abe2519b.gif" in content:
        await message.delete()

    #Toggle FBot
    elif content == "fbot off" or content == "Fbot off" or content == "FBot off":
        setfbot("off", server, channel)
    elif content == "fbot on" or content == "Fbot on" or content == "FBot on":
        setfbot("on", server, channel)
    elif status == "off":
        return
    #elif content != "fbot off":
        #await send("Just a notice to all servers: FBot is migrating from the command `fbot1 on/off` to `fbot on/off`, in the meanwhile use the command `fbot off` to stop spam. Please wait up to 5mins. Sorry for the inconvieniance")

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

    #Call on FBot
    elif startswith("fbot ") or startswith("Fbot ") or startswith("FBot "):
        content = remove(content, 5, 0)
        await send("No {}, {}".format(name, content))
    elif content in fbot:
        await send("Yes {}...?".format(name))
    
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
        elif content == "fuck me" or content == "Fuck me":
            await send("Oh yes, fuck you {}".format(name))
        else:
            await send("Yeah fuck {}".format(name))

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
        

    #Meme talk, Nice, No you, Cool, Lol, Lmao, Lmfao, F, Oof, Bruh, Hmm, Ree
    elif content == "nice" or content == "Nice":
        await message.channel.send("Not nice")
    elif content == "not nice" or content == "Not nice":
        await message.channel.send("Nice")

    elif content == "no u" or content == "No u" or content == "no you" or content == "No you":
        await message.channel.send("No you")

    elif content == "cool" or content == "Cool":
        await message.channel.send("Not cool")
    elif startswith("cooo") or startswith("Cooo"):
        await message.channel.send("Not {}".format(content))

    elif content == "lol" or content == "Lol" or content == "LOL":
        await send("No actually, not funny")
    elif content == "lmao" or content == "Lmao" or content == "LMAO":
        await send("No actually, not funny")
    elif content == "lfmao" or content == "Lmfao" or content == "LMFAO":
        await send("No actually, not funny")
        
    elif content == "f" or content == "F":
        await send("F")

    elif startswith("oof") or startswith("Oof"):
        await send("Oof")

    elif startswith("bru") or startswith("Bru"):
        await send("Yeah {}?".format(content))

    elif startswith("hm"):
        content = remove(content, 1, 0)
        await send("H{} fuck you {}".format(content, name))
    elif startswith("Hm"):
        await send("{} fuck you {}".format(content, name))

    elif startswith("ree") or startswith("Ree"):
        content = remove(content, 1, 0)
        await send("R{}".format(content))

#Client key - this is required to run
client.run('')
