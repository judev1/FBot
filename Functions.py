# Folder: DiscordBots\FBot
#   File: Functions.py

import time, random, datetime, os

class functions():
    def wait(wait):
        time.sleep(wait)

    #Removes known prefix's and suffix's from a string
    def remove(oldtext, front, back):
        length = 0
        text = ""
        for letters in oldtext:
            if length >= front:
                text = "{}{}".format(text, letters)
            length += 1
    
        length = len(text)  
        newtext = ""  
        length = length - back
        for letters in text:
            if length != 0:
                newtext = "{}{}".format(newtext, letters)
                length -= 1
        return newtext

    #Sets up and checks files for severs
    def create(client):
        serverlist = client.guilds
        
        newpath = r"Servers"
        if os.path.exists(newpath):
            print(" > There is already a folder to store server data")
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            print(" > Created a folder to store server data called 'Servers'")

        try:
            file = open("Servers\Server_Names.txt", "r")
            file.close()
            print(" > There is already a file to store server names\n")
        except:
            file = open("Servers\Server_Names.txt", "w+")
            file.close()
            print(" > Created a file to store server names called 'Server_Names.txt'\n")
            
        for server in serverlist:
            serverid = str(server.id)
            info = functions.checkserverid(serverid)
            
            if info[0] == serverid:
                serverid = functions.getserverid(info[0], info[1])
                print(" > {} was already in the datbase".format(server))
            else:
                functions.createserverid(serverid, info[1])
                serverid = functions.getserverid(info[0], info[1])
                print(" > Added {}'s to the database as 'Server {}'".format(server, serverid))  
            
            newpath = r"Servers\{}".format(serverid)
            if os.path.exists(newpath):
                print(" > There is already a folder to store {}'s infomation".format(server))
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                print(" > Created a folder to store {}'s infomation called '{}'".format(server, serverid))            
        
            try:
                file = open("Servers\{}\Data.txt".format(serverid), "r")
                file.close()
                print(" > There is already a file to store {}'s data\n".format(server))
                
            except:
                file = open("Servers\{}\Data.txt".format(serverid), "w+")
                file.close()
                print(" > Created a file to store {}'s data called 'Data.txt'\n".format(server))

    #Checks if there is a name for the gayscale feature
    def checkname(name, server):
        file = open("Servers\{}\Data.txt".format(server), "r")
        data = file.readlines()
        file.close()
        getname = ""
        length = len(data)
        length -= 2
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
        file = open("Servers\{}\Data.txt".format(server), "r")
        data = file.readlines()
        repeat += 1
        getsex = functions.remove(data[repeat], 12, 2)
        return getsex

    #Writes the sexuality of a member if their name isn't found
    def createsex(name, usersex, server):
        file = open("Servers\{}\Data.txt".format(server), "r+")
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
        file = open("Servers\{}\Data.txt".format(server), "w+")
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
        data[length] = "{}Channel ID: '{}'\nChannel Name: '{}'\n".format(lastrow, serverid, name)
        file = open("Servers\{}\Channel_Names.txt".format(serverid), "w+")
        file.writelines(data)
        file.close()
