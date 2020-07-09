# Folder: DiscordBots\FBot
#   File: Functions.py

import os, ctypes, time, datetime

m = 0
h = 0
d = 0

class functions():

    # Removes known prefix's and suffix's from a string
    def remove(text, left_chars, right_chars):
        return text[left_chars:len(text) - right_chars]


    # Sets up and checks files for severs
    def setup():
        newpath = r".servers"
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            os.popen('attrib +h ' + newpath)
            print(" > Created a folder to store server data")
            functions.log("Created a folder to store server data")

        try:
            file = open(".servers\Status.txt", "r")
            file.close()
        except:
            file = open(".servers\Status.txt", "w+")
            data = ("Server: ''\n"
                    "Channel: ''\n"
                    "Status: ''\n")
            file.writelines(data)
            file.close()

            print(" > Created a file to store FBot's channel status")
            functions.log("Created a file to store FBot's channel status\n")

        try:
            file = open(".servers\Data.txt", "r")
            file.close()
        except:
            file = open(".servers\Data.txt", "w+")
            data = ("Server: ''\n"
                    "Modtoggle: ''\n")
            file.writelines(data)
            file.close()

            print(" > Created a file to store FBot's server data")
            functions.log("Created a file to store FBot's server data\n")

    # Sets FBot's status
    def setstatus(server, channel):
        server = str(server.id)
        channel = str(channel.id)
        
        file = open(".servers\Status.txt", "r")
        data = file.readlines()
        file.close

        last = len(data) - 1
        data[last] = ("{}\n"
                      "Server: '{}'\n"
                      "Channel: '{}'\n"
                      "Status: 'off'\n".format(data[last], server, channel))

        file = open(".servers\Status.txt", "w+")
        file.writelines(data)
        file.close()
        functions.log("\nFBot's status has been set to {}, for {}'s {}\n".format(status, server, channel))

    # Checks and gets FBot's status
    def getstatus(server, channel):
        server = str(server.id)
        channel = str(channel.id)
        
        file = open(".servers\Status.txt", "r")
        data = file.readlines()
        file.close
        
        num = 0
        lines = len(data) + 1
        repeat = int(lines / 4)
        
        while repeat != 0:
            if server == functions.remove(data[num], 9, 2):
                num = 1
                repeat = int(lines / 4)
                
                while repeat != 0:
                    if channel == functions.remove(data[num], 10, 2):
                        return True, str(functions.remove(data[num + 1], 9, 2))
                    num += 4
                    repeat -= 1
            num += 4
            repeat -= 1

        return False, ""

    # Changes FBot's status
    def changestatus(status, server, channel):
        server = str(server.id)
        channel = str(channel.id)
        
        file = open(".servers\Status.txt", "r")
        data = file.readlines()
        file.close
        
        num = 0
        lines = len(data) + 1
        repeat = int(lines / 4)
        
        while repeat != 0:
            if server == functions.remove(data[num], 9, 2):
                num = 1
                repeat = int(lines / 4)
                
                while repeat != 0:
                    if channel == functions.remove(data[num], 10, 2):
                        data[num + 1] = "Status: '{}'\n".format(status)

                        file = open(".servers\Status.txt", "w+")
                        file.writelines(data)
                        file.close

                        return
                    num += 4
                    repeat -= 1
            num += 4
            repeat -= 1

    # Sets the modtoggle status
    def setmodtoggle(server):
        server = str(server.id)
        channel = str(channel.id)
        
        file = open(".servers\Data.txt", "r")
        data = file.readlines()
        file.close

        last = len(data) - 1
        data[last] = ("{}\n"
                      "Server: '{}'\n"
                      "Modtoggle: 'off'\n".format(data[last], server))

        file = open(".servers\Data.txt", "w+")
        file.writelines(data)
        file.close()
        functions.log("\nFBot's status has been set to {}, for {}'s {}\n".format(status, server, channel))

    # Checks and gets the modtoggle status
    def getmodtoggle(server):
        server = str(server.id)
        
        file = open(".servers\Data.txt", "r")
        data = file.readlines()
        file.close
        
        num = 0
        lines = len(data) + 1
        repeat = int(lines / 3)
        
        while repeat != 0:
            if server == functions.remove(data[num], 9, 2):
                return True, str(functions.remove(data[num + 2], 12, 2))
            num += 3
            repeat -= 1

        return False, ""

    # Changes the modtoggle status
    def changemodtoggle(status, server):
        server = str(server.id)
        
        file = open(".servers\Data.txt", "r")
        data = file.readlines()
        file.close
        
        num = 0
        lines = len(data) + 1
        repeat = int(lines / 3)
        
        while repeat != 0:
            if server == functions.remove(data[num], 9, 2):
                data[num + 2] = "Modtoggle: '{}'\n".format(status)

                file = open(".servers\Data.txt", "w+")
                file.writelines(data)
                file.close

                return
            
            num += 3
            repeat -= 1

    # Gets a logging channels data
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

    # Checks fo a command
    def fbotcmd(content, cmdname):
        if content.startswith("f "):
            return content.startswith("f bot {}".format(cmdname))
        if content.startswith("<@711934102906994699>"):
            return content.startswith("<@711934102906994699> {}".format(cmdname))
        else:
            return content.startswith("fbot {}".format(cmdname))

    # Logs a message
    def log(message):
        file = open("Logs.txt", "r+")
        data = file.readlines()
        file.writelines(message + "\n")
        file.close()

class time():

    # Gets the start time
    def start():
        timenow = datetime.datetime.now()
        
        global m, h, d, mo
        m = int(timenow.strftime("%M"))
        h = int(timenow.strftime("%H"))
        d = int(timenow.strftime("%d"))
        mo = int(timenow.strftime("%m"))

    # Gets the current time
    def now():
        timenow = datetime.datetime.now()
        m_now = timenow.strftime("%M")
        h_now = timenow.strftime("%H")
        d_now = timenow.strftime("%d")
        mo_now = timenow.strftime("%m")
        return "{}:{}, {}.{} UTC".format(h_now, m_now, d_now, mo_now)

    # Gets the uptime
    def uptime():

        now = datetime.datetime.now()
        m_now = int(now.strftime("%M"))
        h_now = int(now.strftime("%H"))
        d_now = int(now.strftime("%d"))
        mo_now = int(now.strftime("%m"))          

        if mo > mo_now:
            mo_uptime = 60 - mo
            mo_uptime += mo_now
        else:
            mo_uptime = mo_now - mo
        
        if d > d_now:
            if mo == 2:
                d_uptime = 28 - d
            elif mo == 4 or mo == 6 or mo == 9 or mo == 10:
                d_uptime = 31 - d
            else:
                d_uptime = 31 - d
            d_uptime += d_now
            mo_uptime -= 1
        else:
            d_uptime = d_now - d

        if h > h_now:
            h_uptime = 60 - h
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
