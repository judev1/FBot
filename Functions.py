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
        
        newpath = r"Servers"
        if os.path.exists(newpath):
            print(" > There is already a folder to store server data")
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            print(" > Created a folder to store server data called 'Servers'")

        for server in client.guilds:
            server = str(server)
            if server == "IRREGULAR NAME":
                server = "normal name"
            newpath = r"Servers\{}".format(server)
            if os.path.exists(newpath):
                print(" > There is already a folder to store {}'s infomation".format(server))
            if not os.path.exists(newpath):
                os.makedirs(newpath)
                print(" > Created a folder to store {}'s infomation called '{}'".format(server, server))

            try:
                file = open("Servers\{}\Data.txt".format(server), "r")
                file.close()
                
            except:
                file = open("Servers\{}\Data.txt".format(server), "w+")
                file.close()

    #Checks if there is a name for the gayscale feature
    def checkname(name, server):
        server = str(server)
        if server == "IRREGULAR NAME":
            server = "normal name"
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
        server = str(server)
        if server == "IRREGULAR NAME":
            server = "normal name"
        file = open("Servers\{}\Data.txt".format(server), "r")
        data = file.readlines()
        repeat += 1
        getsex = functions.remove(data[repeat], 12, 2)
        return getsex

    #Writes the sexuality of a member if their name isn't found
    def createsex(name, usersex, server):
        server = str(server)
        if server == "IRREGULAR NAME":
            server = "normal name"
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
    def setfbot(status, server):
        server = str(server)
        if server == "IRREGULAR NAME":
            server = "normal name"
        file = open("Servers\{}\Status.txt".format(server), "w+")
        file.writelines(status)
        file.close()

    #Gets FBot's status
    def getfbot(server):
        server = str(server)
        if server == "IRREGULAR NAME":
            server = "normal name"
        file = open("Servers\{}\Status.txt".format(server), "r")
        info = file.readlines()
        return info
