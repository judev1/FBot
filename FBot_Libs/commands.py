import csv

C_NAME = 0 # Name of the command
C_ARGS = 1 # Extra args
C_CAT = 2 # Category
C_SUBCAT = 3 # Sub-Category
C_COOL = 4 # Cooldown
C_PCOOL = 5 # Premium cooldown
C_GUILD = 6 # Guild Only
C_BOT = 7 # Bot Permissions
C_USER = 8 # User Permissions
C_USAGE = 9 # Example Usage(s)
C_LDESC = 10 # Command Long Description
C_SDESC = 11 # Command Short Description

class cmds:
    
    def load():

        global commands, devcmds, categories, perms, devcmdlist
        commands, devcmds, categories, perms, devcmdlist = {}, {}, {}, {}, []
        with open("Info/CSVs/Commands.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:

                perms[row[C_NAME]] = row[C_BOT].split(", ")

                if row[C_ARGS] != "":
                    row[C_ARGS] = " " + row[C_ARGS]

                if row[C_SUBCAT] != "":
                    row[C_SUBCAT] = " - " + row[C_SUBCAT]

                row[C_COOL] = int(row[C_COOL])
                row[C_PCOOL] = int(row[C_PCOOL])

                row[C_GUILD] = "*" + row[C_GUILD] + "*"
                row[C_BOT] = "*" + "*,\n*".join(row[C_BOT].split(", ")) + "*"
                row[C_USER] = "*" + "*,\n*".join(row[C_USER].split(", ")) + "*"

                row[C_USAGE] = row[C_USAGE].replace(" or ", "``````")
                row[C_USAGE] = "```" + row[C_USAGE] + "```"

                if row[C_CAT] != "Dev":
                    commands[row[C_NAME]] = row[1:]
                    data = (row[C_NAME], row[C_ARGS], row[C_SDESC])
                    try: categories[row[C_CAT]].append(data)
                    except: categories[row[C_CAT]] = [data]
                else:
                    devcmds[row[C_NAME]] = row[1:]
                    devcmdlist.append(row)
                
        print(" > Loaded Commands.csv")

    def search(query, dev=False):

        query = query.lower()
        for command in commands:
            if not dev:
                if command[C_CAT] == "Dev":
                    continue
            if command[C_NAME] == query:
                return command
        return None
