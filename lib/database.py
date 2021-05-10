from datetime import datetime
import sqlite3
import time
import os

path = "./data/FBot.db"
conn = sqlite3.connect(path)

with open("./data/FBot.db", "rb") as file:
    now = datetime.now()
    filename = now.strftime("%y-%m-%d %H%M")
    if not os.path.exists(os.path.join("data", "db_backups")):
        os.makedirs(os.path.join("data", "db_backups"))
    with open(f"./data/db_backups/{filename}.db", "wb+") as newfile:
        newfile.writelines(file.readlines())

class db:

    def __init__(self, verbose=True):

        self.conn = conn # For sharing with other cogs/files
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS guilds (
                          guild_id integer NOT NULL,
                          modtoggle string NOT NULL,
                          prefix string NOT NULL,
                          priority string NOT NULL
                          )""")

        c.execute("""CREATE TABLE IF NOT EXISTS channels (
                          guild_id integer NOT NULL,
                          channel_id integer NOT NULL,
                          status string NOT NULL
                          )""")

        c.execute("""CREATE TABLE IF NOT EXISTS users (
                          user_id integer NOT NULL,
                          ppsize integer NOT NULL,
                          commands integer NOT NULL,
                          triggers integer NOT NULL
                          )""")

        c.execute("""CREATE TABLE IF NOT EXISTS counter (
                          guild_id integer NOT NULL,
                          channel_id integer NOT NULL,
                          number integer NOT NULL,
                          user_id integer NOT NULL,
                          record integer NOT NULL
                          )""")

        c.execute("""CREATE TABLE IF NOT EXISTS votes (
                          user_id integer NOT NULL,
                          topvotes integer NOT NULL,
                          dblvotes integer NOT NULL,
                          bfdvotes integer NOT NULL,
                          total_topvotes integer NOT NULL,
                          total_dblvotes integer NOT NULL,
                          total_bfdvotes integer NOT NULL
                          )""")

        conn.commit()
        print(" > Connected to FBot.db") if verbose else False

    def Check_Guilds(self, guilds):
        c = conn.cursor()
        discord_guild_ids = [guild.id for guild in guilds]

        for guild_id in discord_guild_ids:
            t = (guild_id,)
            try:
                c.execute("SELECT * FROM guilds where guild_id=?", t)
                c.fetchone()[0]
            except:
                self.Add_Guild(guild_id)

        count = 0
        c.execute("SELECT guild_id FROM guilds")
        for guild_id in c.fetchall():
            if not (guild_id[0] in discord_guild_ids):
                count += 1
                c.execute("DELETE FROM guilds WHERE guild_id=?", guild_id)
        print("Deleted", count, "guilds from 'guilds'")

        count = 0
        c.execute("SELECT guild_id FROM channels")
        for guild_id in c.fetchall():
            if not (guild_id[0] in discord_guild_ids):
                count += 1
                c.execute("DELETE FROM channels WHERE guild_id=?", guild_id)
        print("Deleted", count, "guild channels from 'channels'")

        count = 0
        c.execute("SELECT guild_id FROM counter")
        for guild_id in c.fetchall():
            if not (guild_id[0] in discord_guild_ids):
                count += 1
                c.execute("DELETE FROM counter WHERE guild_id=?", guild_id)
        print("Deleted", count, "guilds from 'counter'\n")

        conn.commit()

    # General

    def Add_Guild(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("INSERT INTO guilds VALUES(?, 'off', 'fbot', 'all', 1000000);", t)
        c.execute("INSERT INTO counter VALUES(?, 0, 0, 0, 0)", t)
        conn.commit()

    def Remove_Guild(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("DELETE FROM guilds WHERE guild_id=?;", t)
        c.execute("DELETE FROM channels WHERE guild_id=?;", t)
        c.execute("DELETE FROM counter WHERE guild_id=?", t)
        conn.commit()

    def Add_Channel(self, channel_id, guild_id):
        c = conn.cursor()
        t = (guild_id, channel_id)
        try:
            c.execute("SELECT * FROM channels where channel_id=?", [t[1]])
            c.fetchone()[1]
        except:
            c.execute("INSERT INTO channels VALUES (?, ?, 'off')", t)
            conn.commit()

    # Status

    def Change_Modtoggle(self, guild_id, modtoggle):
        c = conn.cursor()
        t = (modtoggle, guild_id)
        c.execute("UPDATE guilds SET modtoggle=? WHERE guild_id=?", t)
        conn.commit()

    def Get_Modtoggle(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT modtoggle FROM guilds WHERE guild_id=?", t)
        return c.fetchone()[0]

    def Change_Status(self, channel_id, status):
        c = conn.cursor()
        t = (status, channel_id)
        c.execute("UPDATE channels SET status=? WHERE channel_id=?", t)
        conn.commit()

    def Get_Status(self, channel_id):
        c = conn.cursor()
        t = (channel_id,)
        c.execute("SELECT status FROM channels WHERE channel_id=?", t)
        return c.fetchone()[0]

    def Get_All_Status(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT channel_id, status FROM channels WHERE guild_id=?", t)
        newdata = []
        for channel in c.fetchall():
            newdata.append((channel[0], channel[1]))
        return newdata

    def Update_Cooldown(self, user_id, cooldown):
        c = conn.cursor()
        t = (time.time() + cooldown, user_id)
        c.execute("UPDATE users SET cooldown=? WHERE user_id=?", t)
        conn.commit()

    def Get_Cooldown(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT cooldown FROM users WHERE user_id=?", t)
        return round(c.fetchone()[0] - time.time(), 2)

    # Users

    def register(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT user_id FROM users WHERE user_id=?", t)
        if c.fetchone() is None:
            t = (user_id,-1,10000,0,0,0,0,"Unemployed","{}","None",0,0,0,0,"{}",0,0)
            marks = ",".join(["?"] * 17)
            c.execute(f"INSERT INTO users VALUES({marks})", t)
            conn.commit()

    def getprofile(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT fbux, netfbux, debt, netdebt, job, degree, degreeprogress FROM users WHERE user_id=?", t)
        return c.fetchone()

    def gettop(self, toptype, amount, obj_id):

        if toptype == "votes":
            TABLE, DATA, ID = "votes", "total_topvotes, total_bfdvotes, total_dblvotes", "user_id"
        elif toptype == "counting":
            TABLE, DATA, ID = "counter", "record", "guild_id"
        if toptype == "votes":
            ORDER = "total_topvotes + total_bfdvotes + total_dblvotes"
        else:
            ORDER = DATA

        c = conn.cursor()
        c.execute(f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC LIMIT {amount}")
        top = c.fetchall()

        c.execute(f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC")
        for rank, data in enumerate(c):
            if data[0] == obj_id:
                selftop = data[1:]
                if toptype == "votes":
                    selftop = sum(selftop)
                else:
                    selftop = selftop[0]
                break

        rank = str(rank + 1)
        if rank.endswith("1") and not rank.endswith("11"): rank += "st"
        elif rank.endswith("2") and not rank.endswith("12"): rank += "nd"
        elif rank.endswith("3") and not rank.endswith("13"): rank += "rd"
        else: rank += "th"

        if toptype == "votes":
            newtop = []
            for data in top:
                if toptype == "votes":
                    item = sum(data[1:])
                newtop.append([data[0], item])
            top = newtop

        return (top, selftop, rank)

    # Voting

    def add_voter(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT user_id FROM votes WHERE user_id=?", t)
        if c.fetchone() is None:
            t = (user_id, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            marks = ",".join(["?"] * 10)
            c.execute(f"INSERT INTO votes VALUES({marks})", t)
            conn.commit()

    def vote(self, user_id, site):
        user_id = int(user_id)
        self.add_voter(user_id)

        c = conn.cursor()
        t = (user_id,)
        c.execute(f"UPDATE votes SET {site}votes={site}votes+1, "
                  f"total_{site}votes=total_{site}votes+1, "
                  f"last{site}vote={time.time()} WHERE user_id=?", t)

        conn.commit()

    def nextvote(self, user_id, site):
        c = conn.cursor()
        user_id = int(user_id)
        t = (user_id,)
        c.execute(f"SELECT last{site}vote FROM votes where user_id=?", t)
        lastvote = c.fetchone()[0]
        if not lastvote: return None
        if site in ["top", "dbl"]:
            nextvote = (lastvote + 60*60*12) - time.time()
        elif site == "bfd":
            lastvote = datetime.fromtimestamp(lastvote)
            now = datetime(lastvote.year, lastvote.month, lastvote.day)
            nextvote = (now.timestamp() + 60*60*24) - time.time()
        rawhours = nextvote / 60 / 60
        mins = round((rawhours - int(rawhours)) * 60)
        hours = int(rawhours)
        if hours < 0 or mins < 0:
            return None
        return (mins, hours)

    # Premium

    def premium(self, user_id):
        if user_id in [671791003065384987, 216260005827969024]:
            return True
        return False

    def getcolour(self, user_id):
        if user_id in [671791003065384987, 216260005827969024]:
            return 0xF42F42 #0xDAA520 #0xA7700B
        return 0xF42F42

    # Prefix

    def Change_Prefix(self, guild_id, prefix):
        c = conn.cursor()
        t = (prefix, guild_id)
        c.execute("UPDATE guilds SET prefix=? WHERE guild_id=?", t)
        conn.commit()

    def Get_Prefix(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT prefix FROM guilds WHERE guild_id=?", t)
        return c.fetchone()[0]

    def Change_Priority(self, guild_id, priority):
        c = conn.cursor()
        t = (priority, guild_id)
        c.execute("UPDATE guilds SET priority=? WHERE guild_id=?", t)
        conn.commit()

    def Get_Priority(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT priority FROM guilds WHERE guild_id=?", t)
        return c.fetchone()[0]

    # ppsize

    def getppsize(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT ppsize FROM users WHERE user_id=?", t)
        return c.fetchone()[0]

    def updateppsize(self, user_id, size):
        c = conn.cursor()
        t = (size, user_id)
        c.execute("UPDATE users SET ppsize=? WHERE user_id=?", t)
        conn.commit()
    
    # Stats

    def usecommand(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("UPDATE users SET commands=commands+1 WHERE user_id=?", t)
        conn.commit()
    
    def usetrigger(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("UPDATE users SET triggers=triggers+1 WHERE user_id=?", t)
        conn.commit()

    # Counting

    def ignorechannel(self, guild_id, channel_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT channel_id FROM counter WHERE guild_id=?", t)
        if channel_id != c.fetchone()[0]: return True
        return False

    def checkdouble(self, guild_id, user_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT user_id FROM counter WHERE guild_id=?", t)
        if user_id == c.fetchone()[0]:
            t = (guild_id,)
            c.execute("UPDATE counter SET number=0, user_id=0 WHERE guild_id=?", t)
            conn.commit()
            return True
        return False

    def getnumber(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT number FROM counter WHERE guild_id=?", t)
        return int(c.fetchone()[0])

    def getuser(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT user_id FROM counter WHERE guild_id=?", t)
        return int(c.fetchone()[0])

    def gethighscore(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT record FROM counter WHERE guild_id=?", t)
        return c.fetchone()[0]

    def gethighscores(self):
        c = conn.cursor()
        c.execute("SELECT guild_id, record FROM counter ORDER BY record DESC LIMIT 5")
        return c.fetchall()

    def resetnumber(self, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("UPDATE counter SET number=0, user_id=0 WHERE guild_id=?", t)
        conn.commit()

    def updatenumber(self, number, author_id, guild_id):
        c = conn.cursor()
        t = (number, author_id, guild_id,)
        c.execute("UPDATE counter SET number=?, user_id=? WHERE guild_id=?", t)
        conn.commit()

    def highscore(self, number, guild_id):
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT record FROM counter WHERE guild_id=?", t)
        if number > c.fetchone()[0]:
            t = (number, guild_id,)
            c.execute("UPDATE counter SET record=? WHERE guild_id=?", t)
            conn.commit()

    def setcountingchannel(self, channel_id, guild_id):
        c = conn.cursor()
        t = (channel_id, guild_id)
        c.execute("UPDATE counter SET channel_id=? WHERE guild_id=?", t)
        conn.commit()