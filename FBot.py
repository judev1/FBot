# Note to self: Remember to delete the token before uploading to GitHub :^)
BOT_TOKEN = ""

# Folder: DiscordBots\FBot
#   File: FBot.py

#FEATURES TO BE ADDED AT SOME POINT:
#BYE, IKR, BRO, WTF, HEY, FUCKING, DANG IT, DUMBASS, SUCK, OH, UWU, WILL, UM, I (word), TRUE, OMG, HE'S/SHE'S, WUT, CALM, ’, ?, DOES, L, E, LEMME, GIMME, HELLO FBOT, YEE, CRINGE, BASED

import discord, random, time, os, sys, datetime
try:
    from PatchNotes import patchnotes as pn
    from Functions import functions as fn
    from BookProgram import book
    from TriggerResponse import trigger_response as tr
except:
    input(" > Unable to install some of the dependencies, shutting down.")
    sys.exit()

client = discord.Client()
remove = fn.remove

create = fn.create
setup = fn.setup

gettime = fn.gettime

setfbot = fn.setfbot
getfbot = fn.getfbot

cmd = fn.fbotcmd

get = fn.get
log = fn.log

tr.load_triggers()

try:
    file = open("Logs.txt", "r+")
except:
    file = open("Logs.txt", "w+")
file.close()

# |---------------------------| FBOT VARIABLES |---------------------------|

#Variables you can change
twss = ["That's big", "that's big", "Thats big", "thats big"]
banned = []
answer = "NO ONE CARES"

#Variables you should not change
fbot = ["fbot", "Fbot",  "fBot",  "fbOt",  "fboT",  "FBot",  "FbOt",  "FboT",  "fBOt",  "fBoT",  "fbOT",  "FBOt",  "FbOT",  "fBOT",  "FBOT", "<@711934102906994699>"]
tf = ["will", "will not"]

fboturl = "https://images.discordapp.net/avatars/711934102906994699/6ab406f40bc3517802fd4402955da1b0.png?size=512"
hitlerurl = "https://pearlsofprofundity.files.wordpress.com/2014/05/adolf-hitler-graphic-1.jpg"

voteurl = "https://top.gg/bot/711934102906994699/vote"
inviteurl = "https://discord.com/oauth2/authorize?client_id=711934102906994699&permissions=8&scope=bot"
githuburl = "https://github.com/judev1/FBot"
topggurl = "https://top.gg/bot/711934102906994699"
serverurl = "https://discord.gg/BDpXRq9"

#Variables for infomation
ready = False
creator = "justjude#2296"
ver = "1.6.7"
lastupdated = "29.06.20"

notices = '''**We are currently holding an event!**
*Use* `FBot events` *or* [*visit FBot's Server for more info*](https://discord.gg/BDpXRq9)

**FBot v{} has been released! as of {}**'''.format(ver, lastupdated)

serverlogs = "720923733132312587"

timenow = datetime.datetime.now()
m = timenow.strftime("%M")
h = timenow.strftime("%H")
d = timenow.strftime("%d")

sessionstart = gettime()
print(" > Session started at {}".format(sessionstart))
log("Session started at {}".format(sessionstart))

# |--------------------------| FBOT CONNECTION |--------------------------|



#When the Client connects to the server
@client.event
async def on_connect():
    
    name = client.user
    print("\n > Began signing into Discord as {}".format(name))
    log("\nAt {}, began signing into Discord as {}".format(gettime(), name))

#When the Server connection is ready  
@client.event
async def on_ready():
    
    name = client.user
    print(" > Finished signing into Discord as {}\n".format(name))
    log("At {}, finished signing into Discord\n".format(gettime()))
        
    create(client)
    create(client)

    global ready
    ready = True
        
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="'FBot help'"))



# |--------------------------| FBOT SERVER LOGS |--------------------------|



#When the Client joins a Guild
@client.event
async def on_guild_join(newguild):

    if ready == False:
        return
    
    channel = get(client, serverlogs)
    await channel.send("I have just been `added` to `{}`".format(newguild))
    log("{} has just been added to a guild ({})".format(client.user, newguild.id))

    create(client)
    create(client)

#When the Client leaves a Guild
@client.event
async def on_guild_remove(newguild):

    if ready == False:
        return

    channel = get(client, serverlogs)
    await channel.send("I have just been `removed` from `{}`".format(newguild))
    log("{} has just been removed from a guild ({})".format(client.user, newguild.id))



# |--------------------------| FBOT MESSENGING |--------------------------|



#Message Replies
@client.event
async def on_message(message):
    
    if ready == False:
        return



# |----------------------------| FBOT SETUP |----------------------------|



    #Variable setups for ease of use
    name = message.author
    name = str(name)
    name = remove(name, 0, 5)

    content = message.content.lower()
    startswith = content.startswith
    endswith = content.endswith
    send = message.channel.send

    server = message.guild
    channel = message.channel

    fn.setup(server, channel)
    data = fn.setup(server, channel)
    
    server = data[0]
    channel = data[1]

    done = True
    
    #Check for a FBot's Status file
    try:
        getfbot(server, channel)
    except:
        setfbot("off", server, channel)

    #Get FBot's Status
    status = getfbot(server, channel)
    status = remove(str(status), 2, 2)



# |---------------------------| FBOT COMMANDS |---------------------------|


    #FBot Patch Notes
    if startswith("fbot p") or startswith("f bot p"):
        if startswith("f "):
            content = remove(content, 6, 0)
        else:
            content = remove(content, 5, 0)

        startswith = content.startswith
        if startswith("pn "):
            content = remove(content, 3, 0)
        elif startswith("patchnotes "):
            content = remove(content, 11, 0)
        elif startswith("patch notes "):
            content = remove(content, 12, 0)
        else:
            done = False
            content = message.content
            startswith = content.startswith

        if done == True:
            pns = pn.get(content)

            if content == "list":
                embed = discord.Embed(title="**Patch Note Arguments**", description="`recent`, `1.1`, `1.2`, `1.3`, `1.4`, `1.5`, `1.6`, `1.6.7`", colour=0xF42F42)
                embed.set_footer(text="PN requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
                await send(embed=embed)

            elif pns != "invalid":
                if content == "recent":
                    content = ver
                    
                embed = discord.Embed(title="FBot Patch Notes", colour=0xF42F42)
                embed.add_field(name="Patch notes for `v{}`".format(content), value="`{}`".format(pns), inline=False)
                embed.set_footer(text="PN requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
                await send(embed=embed)

            else:
                embed = discord.Embed(title="**Error**", description="The argument `'{}'` was not recognised, use `FBot pn list` for all arguments".format(content), colour=0xF42F42)
                embed.set_footer(text="PN requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
                await send(embed=embed)

    #Don't let FBot reply to its self or to other bots
    if message.author == client.user or message.author.bot == True:
        return

    #FBot Commands
    elif cmd(content, "commands") or cmd(content, "command") or cmd(content, "cmd") or cmd(content, "cmds"):
        embed = discord.Embed(title="FBot Commands", description="**Write `FBot ` (the prefix) however you want, I don't care**\n"
                                                                 "*Shorthands for this command are:* `commands`/`command`/`cmds`/`cmd`\n"
                                                                 "\n**General Commands**\n"
                                                                 "`on`/`off`: *Toggles FBot*\n"
                                                                 "`help`/`?`: *Gives some helpful links and commands*\n"
                                                                 "\n**Infomation Commands**\n"
                                                                 "`info`: *Displays some insight into the bot*\n"
                                                                 "`status`: *Displays the status of the bot in the current channel*\n"
                                                                 "`session`/`uptime`: *Gives a session overview*\n"
                                                                 "`version`/`ver`: *Shows the version of the bot*\n"
                                                                 "`ping`: *Shows the current ping for the bot*\n"
                                                                 "`events`/`event`: *Shows any events that are running and gives an overview of it*\n"
                                                                 "`nb`/`noticeboard`/`notice board`: *Shows some cool stuff :)*\n"
                                                                 "`pn`/`patchnotes`/`patch notes` `<ver>`: *Gives you the patchnotes for a version, use recent for the most recent version*\n"
                                                                 "\n**Link Commands**\n"
                                                                 "`links`: *Gives all links*\n"
                                                                 "`vote`: *Gives a link to vote for this FBot*\n"
                                                                 "`invite`: *Gives a link to invite FBot to your server*\n"
                                                                 "`github`: *Gives a link to view FBots Github page*\n"
                                                                 "`top.gg`: *Gives a link to view FBots Top.gg page*\n"
                                                                 "`server`: *Gives a link to join FBots server*\n"
                                                                 "\n**Fun Commands**\n"
                                                                 "`say` `<message>`: *Makes FBot say whatever you want*\n"
                                                                 "`quote`: *Quotes a random part from Mein Kampf*\n".format(status), colour=0xF42F42)
        embed.set_footer(text="Commands requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Help
    elif cmd(content, "help") or cmd(content, "?"):
        embed = discord.Embed(title="FBot Help", description="**Useful Commands**\n"
                                                             "Use `FBot on/off` to toggle fbot\n"
                                                             "Use `FBot cmd` for a list of commands\n\n"
                                                             "**Useful Links**\n"
                                                             "[My Top.gg page]({}) and "
                                                             "[Join my server!]({})\n\n"
                                                             "**You can help FBot too!**\n"
                                                             "[Vote here!]({})".format(topggurl, serverurl, voteurl), colour=0xF42F42)
        embed.set_footer(text="Help requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Info
    elif cmd(content, "info") or cmd(content, "infomation"):
        totalmembers = 0
        for servers in client.guilds:
            if str(servers.id) != "264445053596991498":
                totalmembers += servers.member_count
        embed = discord.Embed(title="FBot Info", colour=0xF42F42)
        embed.add_field(name="Session start", value=sessionstart)
        embed.add_field(name="Servers", value=len(client.guilds) - 1)
        embed.add_field(name="Last Updated", value=lastupdated)
        embed.add_field(name="Uptime", value=fn.uptime(m, h, d))
        embed.add_field(name="Members", value=totalmembers)
        embed.add_field(name="Version", value=ver)
        embed.set_footer(text="Info requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Status
    elif cmd(content, "status"):
        embed = discord.Embed(title="FBot is currently set to `{}` in this channel".format(status), colour=0xF42F42)
        embed.set_footer(text="Status requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Uptime
    elif cmd(content, "uptime") or cmd(content, "session"):
        embed = discord.Embed(title="FBots session", colour=0xF42F42)
        embed.add_field(name="Session start", value=sessionstart)
        embed.add_field(name="Uptime", value=fn.uptime(m, h, d))
        embed.set_footer(text="Session requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Version
    elif cmd(content, "version") or cmd(content, "ver"):
        embed = discord.Embed(title="FBots Version as of {}".format(lastupdated), colour=0xF42F42)
        embed.add_field(name="Version", value=ver)
        embed.set_footer(text="Version requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)    

    #FBot Events
    elif cmd(content, "events") or cmd(content, "event"):
        embed = discord.Embed(title="FBot Events", description="**We are currently holding an event!**\n"
                                                               "We are creating an about page for FBot and we would like your help!\n\n"
                                                               "[Visit FBot's Server for more info](https://discord.gg/BDpXRq9)", colour=0xF42F42)
        embed.set_footer(text="Events requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)
        
    #FBot Notice Board
    elif cmd(content, "nb") or cmd(content, "noticeboard") or cmd(content, "notice board"):
        embed = discord.Embed(title="FBot Notice Board", description=notices, colour=0xF42F42)
        embed.set_footer(text="NB requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)
            
    #FBot Patch Notes
    elif cmd(content, "pn") or cmd(content, "patchnotes") or cmd(content, "patch notes"):
        embed = discord.Embed(title="**Error**", description="You didn't add an argument, for all arguments use `FBot pn list`".format(content), colour=0xF42F42)
        embed.set_footer(text="PN requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Vote
    elif cmd(content, "vote"):
        embed = discord.Embed(title="FBot Vote", description="[Vote for FBot on Top.gg!]({})".format(voteurl), colour=0xF42F42)
        embed.set_footer(text="Vote requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Invite
    elif cmd(content, "invite"):
        embed = discord.Embed(title="FBot Invite", description="[Invite FBot to your server!]({})".format(inviteurl), colour=0xF42F42)
        embed.set_footer(text="Invite requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Github
    elif cmd(content, "github"):
        embed = discord.Embed(title="FBot Github", description="[View FBots code on Github!]({})".format(githuburl), colour=0xF42F42)
        embed.set_footer(text="Github requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Top.gg
    elif cmd(content, "top.gg"):
        embed = discord.Embed(title="FBot Top.gg", description="[View FBots Top.gg page!]({})".format(topggurl), colour=0xF42F42)
        embed.set_footer(text="Top.gg requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)
        
    #FBot Server
    elif cmd(content, "server"):
        embed = discord.Embed(title="FBot Server", description="[Join FBots server!]({})".format(serverurl), colour=0xF42F42)
        embed.set_footer(text="Server requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)

    #FBot Links
    elif cmd(content, "links"):
        embed = discord.Embed(title="FBot Links", description="[Vote for FBot on Top.gg!]({})\n"
                                                              "[Invite FBot to your server!]({})\n"
                                                              "[View FBots code on Github!]({})\n"
                                                              "[View FBots Top.gg page!]({})\n"
                                                              "[Join FBots server!]({})".format(voteurl, inviteurl, githuburl, topggurl, serverurl), colour=0xF42F42)
        embed.set_footer(text="Links requested by {} | Created by {}".format(name, creator), icon_url=fboturl)
        await send(embed=embed)



# |---------------------------| FBOT FEATURES |---------------------------|



    #FBot Say - Makes FBot say anything you input
    elif cmd(content, "say ") and ("@everyone" not in content and "@here" not in content):
        if startswith("f "):
            content = remove(content, 10, 0)
        else:
            content = remove(content, 9, 0)
        await message.delete()
        await send(content)

    #FBot quote
    elif cmd(content, "quote"):
        #Check for Mein_Kampf.txt
        if os.path.exists('./Mein_Kampf.txt'):
            quote = book.quote()
            embed = discord.Embed(title="{}".format(quote), colour=0x000000)
            embed.set_footer(text="- Adolf Hitler".format(name, creator), icon_url=hitlerurl)
            await send(embed=embed)
        else:
            await send("This feature is currently disabled, we hope to re-add it soon")
    
    #Instant link reply
    elif startswith("https://"):
        await send("That's pretty gay ngl")

    #Built-in gifs
    elif content == "smol pp" or content == "Smol pp":
        await send("https://tenor.com/view/tiny-small-little-just-alittle-guy-inch-gif-5676598")
    elif content == "micropenis" or content == "Micropenis":
        await send("https://tenor.com/view/girl-talks-naughty-small-dick-micropenis-gif-11854548")

    #Coin flipper - feet style
    elif content == "feet pics":
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

    # [dev] Reload triggers.
    elif content.lower() == "fbotdev treload":
        start = time.time()
        tr.load_triggers()
        print("[dev] treload command by " + name)
        await send("`[dev] Reloaded triggers.csv in " + str(round(time.time() - start, 4)*1000) + "ms`")

    #Toggle FBot Triggers
    elif cmd(content, "off"):
        setfbot("off", server, channel)
    elif cmd(content, "on"):
        setfbot("on", server, channel)
    elif status == "off":
        return


# |---------------------------| FBOT TRIGGERS |---------------------------|

    else:
        trigger_detected, response = tr.trigger_respond(message.content)
        if trigger_detected:
            response = response.replace("{username}", name)
            response = response.replace("{ping}", "`" + str(int(client.latency*100000)/100) + "ms`")
            response = response.replace("{answer}", answer)
            await send(response)

#Client key - this is required to run
client.run(BOT_TOKEN)
