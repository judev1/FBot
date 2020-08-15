import os, random

capitals = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"
            "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X"
            "Y", "Z"]
class book():
        def quote():
                file = open("./Info/Mein_Kampf.txt", "r")

                book = file.readlines()

                length = len(book) - 1
                
                valid = False
                while valid == False:
                        
                        num = random.randint(11, length)
                        
                        capline = num
                        capitalfound = False
                        while capitalfound == False:
                                cappos = 0
                                for characters in book[capline]:
                                        cappos += 1
                                        for letters in capitals:
                                                if letters == characters:
                                                        capitalfound = True
                                                        break
                                        if capitalfound == True:
                                                break
                                if capitalfound == False:
                                        capline -= 1


                        holderpos = cappos
                        dotline = capline
                        dotfound = False
                        while dotfound == False:
                                dotpos = 0
                                for characters in book[dotline]:
                                        dotpos += 1
                                        if dotpos >= holderpos:
                                                if characters == ".":
                                                        dotfound = True
                                                        break
                                        if dotfound == True:
                                                break
                                if dotfound == False:
                                        holderpos = 0
                                        dotline += 1

                        line = capline
                        quote = ""
                        quotefound = False
                        while quotefound == False:
                                pos = 0
                                for letters in book[line]:
                                        pos += 1
                                        if pos >= cappos:
                                                quote = "{}{}".format(quote, letters)
                                                if letters == ".":
                                                        quotefound = True
                                        if quotefound == True:
                                                break
                                if quotefound == False:
                                        cappos = 1
                                        line += 1

                        #newquote = ""
                        #for letters in quote:
                                #if letters != enter:
                                        #newquote = "{}{}".format(newquote, letters)
                                  
                        if len(quote) > 256:
                                valid = False
                        else:
                                valid = True

                return quote

