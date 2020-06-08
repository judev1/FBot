# Folder: DiscordBots\FBot
#   File: FBot.py

from Functions import functions as fn
import discord, random, time, os

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


#Variables you can change
sexuality = ["gay", "straight", "definitley not straight", "I have no fucking clue", "like mostly gay", "half gay", "just a pedo", "bixsexual probaly"]
twss = ["That's big", "that's big", "Thats big", "thats big"]
banned = []

#Variables you should not change
fbot = ["fbot", "Fbot",  "fBot",  "fbOt",  "fboT",  "FBot",  "FbOt",  "FboT",  "fBOt",  "fBoT",  "fbOT",  "FBOt",  "FbOT",  "fBOT",  "FBOT"]
tf = ["will", "will not"]

creator = "justjude#2296"
ver = "1.4.0"


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
    elif content == "fbot help" or content == "Fbot help" or content == "FBot help":
        embed = discord.Embed(title="FBot Help", description="**Use '`fbot on/off`' to toggle fbot**\n\n"
                                                             "**For more infomation go to:**\n"
                                                             "[*My Github*](https://github.com/judev1/FBot), "
                                                             "[*My top.gg*](https://top.gg/bot/711934102906994699), or "
                                                             "[*Contact Me!*](https://discord.gg/BDpXRq9)\n\n"
                                                             "**You can help FBot too!**\n"
                                                             "[*By voting!*](https://top.gg/bot/711934102906994699/vote)", colour=0xF42F42)
        embed.set_footer(text="Help requested by {} | FBot v{}".format(message.author, ver))
        await message.channel.send(embed=embed)

    #FBot Info
    elif content == "fbot info" or content == "Fbot info" or content == "FBot info":
        totalmembers = 0
        for servers in client.guilds:
            totalmembers += servers.member_count
        embed = discord.Embed(title="TOTAL SERVER COUNT: `{}`\nTOTAL MEMBER COUNT: `{}`\nPING: `{}ms`".format(len(client.guilds), totalmembers, ping(message.created_at)), colour=0xF42F42)
        embed.set_footer(text="Created by {} | FBot v{}".format(creator, ver))
        await message.channel.send(embed=embed)

    #FBot Vote
    elif content == "fbot vote" or content == "Fbot vote" or content == "FBot vote":
        embed = discord.Embed(title="FBot Vote", description="[*Vote for fbot here!*](https://top.gg/bot/711934102906994699/vote)", colour=0xF42F42)
        embed.set_footer(text="Vote requested by {} | FBot v{}".format(message.author, ver))
        await message.channel.send(embed=embed)
    
    #Toggle FBot
    elif content == "fbot off" or content == "Fbot off" or content == "FBot off":
        setfbot("off", server, channel)
    elif content == "fbot on" or content == "Fbot on" or content == "FBot on":
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
        
        
        info = checkname(name, server)
        usersex = getsex(info[0], info[1], server)
        if username == info[0]:
            await send("{}'s sexuality is: {}".format(info[0], usersex))
        else:
            await send("{} wasn't in the database".format(name))

    #Gifs
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
    elif startswith("Take me home") or startswith("Take me home"):
        await send("Country roads")

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
    #elif fbot in content:
        #await send("Yes {}...?".format(name))
    
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
            await send("Oh yes, fuck me, fuck me hard daddy")
        elif content == "fuck me " or content == "Fuck me ":
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

    #Meme talk: Nice, No you, Cool, Die, Lol, Lmao, Lmfao, Hehe, Haha, F, Oof, Bruh, Hmm, Ree
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

    elif content == "hehe" or content == "Hehe" or startswith("heh") or startswith("Heh"):
        content = remove(content, 1, 0)
        await send("H{}, you sound pathetic, fuck you".format(content))
    elif content == "haha" or content == "Haha" or content == "HAHA" or startswith("hah") or startswith("Hah") or startswith("HAH"):
        content = remove(content, 1, 0)
        await send("H{}, you sound pathetic, fuck you".format(content))

    elif startswith("die ") or startswith("Die "):
        content = remove(content, 4, 0)
        await send("Yes die {}".format(content))
    elif content == "die" or content == "Die":
        await send("Die motherfucker")
        
    elif content == "f" or content == "F":
        await send("F")

    elif startswith("oof") or startswith("Oof"):
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


#Client key - this is required to run
client.run('')
#Testing FBot - a seperate client key I have for testing only
#client.run('')
