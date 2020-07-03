# Folder: DiscordBots\FBot
#   File: Functions.py

import time, random, datetime, os, ctypes

class functions():

    #Removes known prefix's and suffix's from a string
    def remove(text, left_chars, right_chars):
        return text[left_chars:len(text) - right_chars]


    #Sets up and checks files for severs
    def create(client):
        serverlist = client.guilds
        
        newpath = r".servers"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            os.popen('attrib +h ' + newpath)
            #print(" > Created a folder to store server data")
            functions.log("Created a folder to store server data")

        try:
            file = open(".servers\Server_Names.txt", "r")
            file.close()
        except:
            file = open(".servers\Server_Names.txt", "w+")
            file.close()
            #print(" > Created a file to store server names\n")
            functions.log("Created a file to store server data\n")
            
        for server in serverlist:
            serverid = str(server.id)
            info = functions.checkserverid(serverid)
            
            if info[0] == serverid:
                serverid = functions.getserverid(info[0], info[1])
            else:
                functions.createserverid(serverid, info[1])
                serverid = functions.getserverid(info[0], info[1])
                #print(" > {} has been added to the database".format(server))
                functions.log("Added {} to the database".format(serverid))
            
            newpath = r".servers\.{}".format(serverid)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                os.popen('attrib +h ' + newpath)
                #print(" > Created a folder to store {}'s data".format(server))
                functions.log("Created a folder to store {}'s data".format(serverid))


    #Channel setup
    def setup(server, channel):
        fn = functions
        checkserver = fn.checkserverid
        getserver = fn.getserverid
        createserver = fn.createserverid
        checkchannel = fn.checkchannelid
        getchannel = fn.getchannelid
        createchannel = fn.createchannelid
        
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
            file = open(".servers\.{}\Channel_Names.txt".format(server), "r")
            file.close()
        except:
            file = open(".servers\.{}\Channel_Names.txt".format(server), "w+")
            #print(" > Created a file to store {}'s channel data".format(server))
            functions.log("\nCreated a file to store {}'s channel data".format(server))
            file.close()  
                
        #Check for the Channel's data
        channelid = str(channel.id)
        info = checkchannel(channelid, server)
                
        if info[0] == channelid:
            channel = getchannel(info[0], info[1], server)
        else:
            createchannel(channelid, info[1], server)
            channel = getchannel(info[0], info[1], server)
            #print(" > Added {}'s {} to the database".format(server, channel))
            functions.log("Added {}'s {} to the database".format(server, channel))
            
        #Create a folder for the Channel
        newpath = r".servers\.{}\.{}".format(server, channel)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            os.popen('attrib +h ' + newpath)
            #print(" > Created a folder to store {}'s channel: {}'s data".format(server, channel))
            functions.log("Created a folder to store {}'s {}'s data".format(server, channel))
        data = [server, channel]
        return data


    #Creates a file for FBot's status
    def setfbot(status, server, channel):
        try:
            file = open(".servers\.{}\.{}\Status.txt".format(server, channel), "r+")
            file.close()
            file = open(".servers\.{}\.{}\Status.txt".format(server, channel), "w+")
            functions.log("\nFBot's status has been set to {}, for {}'s {}\n".format(status, server, channel))
        except:
            file = open(".servers\.{}\.{}\Status.txt".format(server, channel), "w+")
            functions.log("\nCreated an FBot Status file for {}'s {}".format(server, channel))
        file.writelines(status)
        file.close()

    #Gets FBot's status
    def getfbot(server, channel):
        file = open(".servers\.{}\.{}\Status.txt".format(server, channel), "r")
        info = file.readlines()
        return info


    #Checks for the Server ID
    def checkserverid(name):
        name = str(name)
        file = open(".servers\Server_Names.txt", "r")
        data = file.readlines()
        file.close()
        getname = ""
        length = len(data)
        length -= 1
        repeat = -1
        while repeat != length:
            repeat += 2
            getname = functions.remove(data[repeat], 14, 2)
            getname = str(getname)
            if name == getname:
                break
        info = [getname, repeat]
        return info

    #Gets the Server ID
    def getserverid(name, repeat):
        file = open(".servers\Server_Names.txt", "r")
        data = file.readlines()
        repeat -= 1
        getid = functions.remove(data[repeat], 12, 2)
        getid = "server_{}".format(getid)
        return getid

    #Creates a Server ID
    def createserverid(name, serverid):
        file = open(".servers\Server_Names.txt", "r+")
        data = file.readlines()
        file.close()
        length = len(data)
        serverid += 1
        serverid /= 2
        serverid += 1
        serverid = int(serverid)
        if length != 0:
            length -= 1
            lastrow = data[length]
        else:
            lastrow = ""
            data = [""]
        data[length] = "{}Server ID: '{}'\nServer Name: '{}'\n".format(lastrow, serverid, name)
        file = open(".servers\Server_Names.txt", "w+")
        file.writelines(data)
        file.close()


    #Checks for the Channel ID
    def checkchannelid(name, serverid):
        name = str(name)
        file = open(".servers\.{}\Channel_Names.txt".format(serverid), "r")
        data = file.readlines()
        file.close()
        getname = ""
        length = len(data)
        length -= 1
        repeat = -1
        while repeat != length:
            repeat += 2
            getname = functions.remove(data[repeat], 15, 2)
            getname = str(getname)
            if name == getname:
                break
        info = [getname, repeat]
        return info

    #Gets the Channel ID
    def getchannelid(name, repeat, serverid):
        file = open(".servers\.{}\Channel_Names.txt".format(serverid), "r")
        data = file.readlines()
        repeat -= 1
        getid = functions.remove(data[repeat], 13, 2)
        getid = "channel_{}".format(getid)
        return getid

    #Creates a Channel ID
    def createchannelid(name, channelid, serverid):
        file = open(".servers\.{}\Channel_Names.txt".format(serverid), "r+")
        data = file.readlines()
        file.close()
        length = len(data)
        channelid += 1
        channelid /= 2
        channelid += 1
        channelid = int(channelid)
        if length != 0:
            length -= 1
            lastrow = data[length]
        else:
            lastrow = ""
            data = [""]
        data[length] = "{}Channel ID: '{}'\nChannel Name: '{}'\n".format(lastrow, channelid, name)
        file = open(".servers\.{}\Channel_Names.txt".format(serverid), "w+")
        file.writelines(data)
        file.close()

    #Gets the channels data
    def get(client, channelid):
        guilds = client.guilds
        num = -1
        for guild in guilds:
            num += 1
            if str(guild.id) == "717735765936701450":
                break
            
        channels = guild.channels
        num = -1
        for channel in channels:
            num += 1
            if str(channel.id) == channelid:
                break

        channel = channels[num]
        return channel

    #Checks fo a command
    def fbotcmd(content, cmdname):
        if content.startswith("f "):
            return content.startswith("f bot {}".format(cmdname))
        if content.startswith("<@!"):
            return content.startswith("<@!711934102906994699> {}".format(cmdname))
        else:
            return content.startswith("fbot {}".format(cmdname))

    #Logs a message
    def log(message):
        file = open("Logs.txt", "r+")
        data = file.readlines()
        file.writelines(message + "\n")
        file.close()

    #Gets the current time
    def gettime():
        timenow = datetime.datetime.now()
        m = timenow.strftime("%M")
        h = timenow.strftime("%H")
        d = timenow.strftime("%d")
        mo = timenow.strftime("%m")
        return "{}:{}, {}.{} UTC".format(h, m, d, mo)

    #Gets the uptime
    def uptime(m, h, d):
        
        now = datetime.datetime.now()
        now_m = int(now.strftime("%M"))
        now_h = int(now.strftime("%H"))
        now_d = int(now.strftime("%d"))
        m = int(m)
        h = int(h)
        d = int(d)

        if d > now_d:
            d = 30 - d
            d += now_d         
        else:
            d = now_d - d

        if h > now_h:
            h = 60 - h
            h += now_h
            d -= 1
        else:
            h = now_h - h

        if m > now_m:
            m = 60 - m
            m += now_m
            h -= 1
        else:
            m = now_m - m

        ds = ""
        hs = ""
        ms = ""
        uptime = ""
        
        if d != 1:
            ds = "s"
        if h != 1:
            hs = "s"
        if  m != 1:
            ms = "s"
        
        if d > 0:
            uptime = "{} day{}, {} hour{}".format(d, ds, h, hs)

        elif h > 0:
            uptime = "{} hour{}, {} minute{}".format(h, hs, m, ms)

        else:
            uptime = "{} minute{}".format(m, ms)

        return uptime
