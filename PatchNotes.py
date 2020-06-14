# Folder: DiscordBots\FBot
#   File: Patch Notes.py

def v1():
    pn = ("Created FBot\n"
          "'Creation Update'\n"
          "- A variety of snappy replies to commonly used phrases\n"
          "- FBot can be turned on/off in a server with some exceptions for unusual names which have to be manually added\n"
          "- Features including Gayscale, Feet pics and Link disaproval have been added\n"
          "- And more!\n"
          "Main: 368 lines (+368)\n"
          "Func: 125 lines (+125)\n"
          "Totl: 493 lines (+493)")
    return pn

def v2():
    pn = ("What's new in v1.2?\n"
          "'Control Update'*\n"
          "- Added a 'Call on FBot' feature\n"
          "- Added new trigger words: I would, U, Ur, No you, Cool, Lol, Lmao, Lmfao, F and Ree\n"
          "- Fixed up the layout\n"
          "- Fixed up some typos\n"
          "Main: 418 lines (+050)\n"
          "Func: 229 lines (+104)\n"
          "Totl: 647 lines (+154)")
    return pn

def v3():
    pn = ("What's new in v1.3?\n"
          "'Fix Update'\n"
          "- Added support for every server and channel name\n"
          "- Changed it so that FBot is toggleable in each channel\n"
          "- Changed the prefix from 'fbot1' to 'fbot'\n"
          "- Added new trigger words: Let us and an Aki bot replier\n"
          "- Fixed up the layout\n"
          "- Fixed up some typos\n"
          "- Did maintenance things\n"
          "Main: 456 lines (+38)\n"
          "Func: 265 lines (+36)\n"
          "Totl: 721 lines (+74)")
    return pn

def v4():
    pn = ("**What's new in v1.4?**\n"
          "*'Infomation Update'*\n"
          "- Added new commands, help, info and vote\n"
          "- Added Hehe and Haha\n"
          "- Improved the call on FBot response\n"
          "- Improved West Virginia\n"
          "- Added better Fuck me support\n"
          "- Simplified Yeah response - It was more of an inside joke\n"
          "- Removed a few more inside jokes\n"
          "- Improved Gayscale a bit\n"
          "- Decreased Feet pics waiting time\n"
          "- Fixed a few minor bugs\n"
          "- Simplified some of the code\n"
          "- Made some of the code more efficient\n"
          "- Organised  the code a bit better\n"
          "- Removed an old message\n"
          "- Fixed a typo or two\n"
          "Main: 495 lines (+39)\n"
          "Func: 304 lines (+39)\n"
          "Totl: 799 lines (+78)")
    return pn

def v5():
    pn = ("What's new in v1.5?\n"
          "'Commands Update'\n"
          "- Added new commands: notice board, events, status, ping, commands\n"
          "- Fixed and added to previous commands: Help and info\n"
          "- New trigger words: Smiley faces, Hello, Hi, Welcome, Thanks, Thank you, Tysm, Ooo, Stfu\n"
          "- Improved Hehe and Haha by a shit ton, can guess it most of the time\n"
          "- Improved the call on FBot feature"
          "- Improved Fuck you added F u\n"
          "- Added a plain fuck trigger word\n"
          "- Improved Oof\n"
          "- Added a feature to check if any spelling of FBot can be found in a phrase, for commands mainly\n"
          "- Simplified some of the code\n"
          "- Fixed Gayscale, again\n"
          "- Fixed some of the wording\n"
          "- Fixed a minor error\n"
          "Main: 637 lines (+142)\n"
          "Func: 319 lines (+015)\n"
          "Totl: 956 lines (+157)")
    return pn

def v6():
    pn = ("What's new in v1.6?\n"
          "'Code Update'\n"
          "- Added new commands: patch notes, say and quote\n"
          "- Fixed and added the quote feature and created a program to look for the quote\n"
          "- Created a program to store and retrieve patch notes\n"
          "- Added F Bot for people who don't realise it's one word\n"
          "- Fixed the F u/me/FBot Trigger (it didn't actually work)\n"
          "- Added more question trigger words: Can, Will, Should, Could, Would, changed the answers too\n"
          "- Fixed Cool and I, and added I should, I could, I would\n"
          "- Simplified some code\n"
          "- Tidied up the code\n"
          "- Made the code easier to read\n"
          "Main:  786 lines (+149)\n"
          "Func:  319 lines (+002)\n"
          "PatN:  125 lines (+125\n"
          "BkPg:   82 lines (+082)\n"
          "Totl: 1314 lines (+358)")
    return pn

class patchnotes():

    def get(content):
        
        if content == "recent":
            return v6()
        elif content == "1.1":
            return v1()
        elif content == "1.2":
            return v2()
        elif content == "1.3":
            return v3()
        elif content == "1.4":
            return v4()
        elif content == "1.5":
            return v5()
        elif content == "1.6":
            return v6()
        else:
            return "invalid"
