# Folder: DiscordBots\FBot
#   File: Functions.py

import time, random, datetime, os

fbot = ["fbot", "Fbot",  "fBot",  "fbOt",  "fboT",  "FBot",  "FbOt",  "FboT",  "fBOt",  "fBoT",  "fbOT",  "FBOt",  "FbOT",  "fBOT",  "FBOT",
        "f bot", "F bot",  "f Bot",  "f bOt",  "f boT",  "F Bot",  "F bOt",  "F boT",  "f BOt",  "f BoT",  "f bOT",  "F BOt",  "F bOT",  "f BOT",  "F BOT",
        "<@711934102906994699>", "<@!711934102906994699>"]

class functions():

    # Removes known prefixes and suffixes from a string
    def remove(old_text, left_chars, right_chars):
        return (old_text[:len(old_text)-right_chars])[left_chars:]
        # [:len(old_text)-right_chars] removes right chars
        # [left_chars:] removes left chars


    #Sets up and checks files for severs
    def create(client):
        serverlist = client.guilds
        
        newpath = r"Servers"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            print(" > Created a folder to store server data")

        try:
            file = open("Servers\Server_Names.txt", "r")
            file.close()
        except:
            file = open("Servers\Server_Names.txt", "w+")
            file.close()
            print(" > Created a file to store server names\n")
            
        for server in serverlist:
            serverid = str(server.id)
            info = functions.checkserverid(serverid)
            
            if info[0] == serverid:
                serverid = functions.getserverid(info[0], info[1])
            else:
                functions.createserverid(serverid, info[1])
                serverid = functions.getserverid(info[0], info[1])
                print(" > Added {}'s to the database".format(server))  
            
            newpath = r"Servers\{}".format(serverid)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                print(" > Created a folder to store {}'s infomation".format(server))


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
        data = [server, channel]
        return data


    #Checks if there is a name for the gayscale feature
    def checkname(name, server):
        try:
            file = open("Servers\{}\Gayscale.txt".format(server), "r")           
        except:
            file = open("Servers\{}\Gayscale.txt".format(server), "w+")
            print(" > Created a file to store {}'s gayscale data\n".format(server))
        data = file.readlines()
        file.close()
        getname = ""
        length = len(data) - 2
        repeat = -2
        while repeat != length:
            repeat += 2
            getname = functions.remove(data[repeat], 7, 2)
            if name == getname:
                break
        info = [getname, repeat]
        return info

    #Gets the sexuality of a member if their name was found
    def getsex(name, repeat, server):
        file = open("Servers\{}\Gayscale.txt".format(server), "r")
        data = file.readlines()
        repeat += 1
        getsex = functions.remove(data[repeat], 12, 2)
        return getsex

    #Writes the sexuality of a member if their name isn't found
    def createsex(name, usersex, server):
        file = open("Servers\{}\Gayscale.txt".format(server), "r+")
        data = file.readlines()
        file.close()
        length = len(data)
        if length != 0:
            length -= 1
            lastrow = data[length]
        else:
            lastrow = ""
            data = [""]
        data[length] = "{}Name: '{}'\nSexuality: '{}'\n".format(lastrow, name, usersex)
        file = open("Servers\{}\Gayscale.txt".format(server), "w+")
        file.writelines(data)
        file.close()


    #Creates a file for FBot's status
    def setfbot(status, server, channel):
        file = open("Servers\{}\{}\Status.txt".format(server, channel), "w+")
        file.writelines(status)
        file.close()

    #Gets FBot's status
    def getfbot(server, channel):
        file = open("Servers\{}\{}\Status.txt".format(server, channel), "r")
        info = file.readlines()
        return info


    #Checks for the Server ID
    def checkserverid(name):
        name = str(name)
        file = open("Servers\Server_Names.txt", "r")
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
        file = open("Servers\Server_Names.txt", "r")
        data = file.readlines()
        repeat -= 1
        getid = functions.remove(data[repeat], 12, 2)
        getid = "Server {}".format(getid)
        return getid

    #Creates a Server ID
    def createserverid(name, serverid):
        file = open("Servers\Server_Names.txt", "r+")
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
        file = open("Servers\Server_Names.txt", "w+")
        file.writelines(data)
        file.close()


    #Checks for the Channel ID
    def checkchannelid(name, serverid):
        name = str(name)
        file = open("Servers\{}\Channel_Names.txt".format(serverid), "r")
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
        file = open("Servers\{}\Channel_Names.txt".format(serverid), "r")
        data = file.readlines()
        repeat -= 1
        getid = functions.remove(data[repeat], 13, 2)
        getid = "Channel {}".format(getid)
        return getid

    #Creates a Channel ID
    def createchannelid(name, channelid, serverid):
        file = open("Servers\{}\Channel_Names.txt".format(serverid), "r+")
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
        file = open("Servers\{}\Channel_Names.txt".format(serverid), "w+")
        file.writelines(data)
        file.close()

    #Gets the ping
    def ping(timestart):
        
        timenow = datetime.datetime.now()
        timethen_m = int(timestart.strftime("%M"))
        timenow_m = int(timenow.strftime("%M"))
        timethen_s = int(timestart.strftime("%S"))
        timenow_s = int(timenow.strftime("%S"))
        timethen_ms = int(timestart.strftime("%f"))
        timenow_ms = int(timenow.strftime("%f"))
        
        if timethen_m > timenow_m:
            minutes = 60 - timethen_m
            minutes += timenow_m          
        else:
            minutes = timenow_m - timethen_m
            
        if timethen_s > timenow_s:
            seconds = 60 - timethen_s
            seconds += timenow_s
            minutes -= 1
        else:
            seconds = timenow_s - timethen_s

        timethen_ms /= 1000
        timenow_ms /= 1000
        if timethen_ms > timenow_ms:
            ms = 1000 - timethen_ms
            ms += timenow_ms
            seconds -= 1
        else:
            ms = timenow_ms - timethen_ms

        ms = ms + (minutes * 1000 * 60)
        ms = ms + (seconds * 1000)
        ms = round(ms)

        return ms

    #Checks if FBot is in content
    def fbotin(content):
        for fbots in fbot:
            if fbots in content:
                return True
        return False

    #Checks if FBot is in a command
    def fbotcmd(content, name):
        for fbots in fbot:
            cmdname = "{} {}".format(fbots, name)
            if content == cmdname:
                return True
        return False
