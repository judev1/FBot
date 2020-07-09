# Folder: DiscordBots\FBot
#   File: Triggers.py

import csv

class trigger_response:
    
    # Load triggers from triggers.csv file
    def trigger_load():
        
        T_MESSAGE = 0
        T_TYPE = 1 # whole / start / end / any / repeat / letters / replace
        T_CASE = 2 # any / exact
        T_RESPONSE = 3

        global triggers
        global all_aliases
        triggers = []
        all_aliases = []
        with open("triggers.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                if row[0] == "":
                    print("[WARNING] Empty trigger found in CSV file, please delete ASAP\n")
                else:
                    row_to_add = row
                    row_to_add[T_TYPE] = row_to_add[T_TYPE].lower()
                    row_to_add[T_CASE] = row_to_add[T_CASE].lower()
                    if row_to_add[T_CASE] == "any":
                        row_to_add[T_MESSAGE] = row_to_add[T_MESSAGE].lower()
                    triggers.append(row_to_add)
                    all_aliases += (row_to_add[0].split("\\"))
            csv_file.close()
        print(" > Loaded Triggers.csv")
        # for alias in all_aliases:
        #    print(alias, end = ", ")
        # print("\n")
        

    # Check if a message contains a trigger and return True/False + response
    def trigger_respond(message):
        T_MESSAGE = 0
        T_TYPE = 1 # whole / start / end / any / repeat / letters / replace
        T_CASE = 2 # any / exact
        T_RESPONSE = 3

        debug_mode = False
        
        print("Trigger_respond called\nMessage is " + message) if debug_mode else False
        for trigger in triggers:
            if trigger[T_CASE] == "any":
                message_check = message.lower()
            else:
                message_check = message
            
            type_check = False
            trigger_aliases = trigger[T_MESSAGE].split("\\")
            alias_used = ""
            for alias in trigger_aliases:
                print("msg: " + message_check + ", alias: " + alias) if debug_mode else False
                if trigger[T_TYPE] == "whole" and message_check == alias:
                    type_check = True
                    break
                elif trigger[T_TYPE] == "start" and message_check.startswith(alias):
                    type_check = True
                    break
                elif trigger[T_TYPE] == "end" and message_check.endswith(alias):
                    type_check = True
                    break
                #elif trigger[T_TYPE] == "any" and alias in message_check:
                    #type_check = True
                    #break
                elif trigger[T_TYPE] == "repeat":
                    alias_split = alias.split("~")
                    if message_check.startswith(alias_split[0]) and message_check.endswith(alias_split[1]):
                        type_check = True
                        break
                elif trigger[T_TYPE] == "letters":
                    if message_check == "":
                        break
                    for letter in alias:
                        message_check = message_check.replace(letter, "")
                    if message_check == "":
                        type_check = True
                        break
                elif trigger[T_TYPE] == "replace" and alias in message_check:
                    trigger[T_RESPONSE] = message_check.replace(alias, trigger[T_RESPONSE])
                    type_check = True
                    break
                    

            if type_check:
                alias_used = alias
                print("type_check is: " + str(type_check)) if debug_mode else False
                print("alias_used is: " + alias_used) if debug_mode else False
                response = trigger[T_RESPONSE]
                # {username}, {ping} and {answer} are replaced in fbot.py
                response = response.replace("{after}", message[len(alias_used):])
                response = response.replace("{message}", message)
                return True, response
        return False, ""
