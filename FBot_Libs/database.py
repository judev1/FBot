from datetime import datetime
import sqlite3
import time
import os

path = "./Info/FBot.db"
conn = sqlite3.connect(path)

with open("./Info/FBot.db", "rb") as file:
    now = datetime.now()
    filename = now.strftime("%y-%m-%d %H%M")
    if not os.path.exists(os.path.join("Info", "db_backups")):
        os.makedirs(os.path.join("Info", "db_backups"))
    with open(f"./Info/db_backups/{filename}.db", "wb+") as newfile:
        newfile.writelines(file.readlines())

class db:

    def __init__(self, verbose=True):

        self.conn = conn # For sharing with other cogs/files
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS guilds (
                          guild_id integer NOT NULL,
                          modtoggle string NOT NULL,
                          prefix string NOT NULL,
                          priority string NOT NULL,
                          multiplier integer NOT NULL
                          )""")

        c.execute("""CREATE TABLE IF NOT EXISTS channels (
                          guild_id integer NOT NULL,
                          channel_id integer NOT NULL,
                          status string NOT NULL
                          )""")

        c.execute("""CREATE TABLE IF NOT EXISTS users (
                          user_id integer NOT NULL,
                          ppsize integer NOT NULL,
                          multiplier integer NOT NULL,
                          fbux integer NOT NULL,
                          debt integer NOT NULL,
                          netfbux integer NOT NULL,
                          netdebt integer NOT NULL,
                          job string NOT NULL,
                          jobs string NOT NULL,
                          degree string NOT NULL,
                          lastwork integer NOT NULL,
                          laststudy integer NOT NULL,
                          degreeprogress integer NOT NULL,
                          cooldown integer NOT NULL,
                          inventory string NOT NULL,
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

    # Economy

    def register(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT user_id FROM users WHERE user_id=?", t)
        if c.fetchone() is None:
            t = (user_id,-1,10000,0,0,0,0,"Unemployed","{}","None",0,0,0,0,"{}",0,0)
            marks = ",".join(["?"] * 17)
            c.execute(f"INSERT INTO users VALUES({marks})", t)
            conn.commit()

    def increasemultiplier(self, user_id, guild_id, number):
        c = conn.cursor()
        t = (number, user_id)
        c.execute("UPDATE users SET multiplier=multiplier+? WHERE user_id=?;", t)
        t = (number, guild_id)
        c.execute("UPDATE guilds SET multiplier=multiplier+? WHERE guild_id=?", t)
        conn.commit()

    def getprofile(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT fbux, netfbux, debt, netdebt, job, degree, degreeprogress FROM users WHERE user_id=?", t)
        return c.fetchone()

    def getbal(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT fbux, debt FROM users WHERE user_id=?", t)
        return c.fetchone()

    def getmultis(self, user_id, guild_id):
        usermulti = self.getusermulti(user_id)
        c = conn.cursor()
        t = (guild_id,)
        c.execute("SELECT multiplier FROM guilds WHERE guild_id=?", t)
        return (usermulti, c.fetchone()[0]/(10**6))

    def getusermulti(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT multiplier FROM users WHERE user_id=?", t)
        return c.fetchone()[0]/(10**4)

    def getjobmulti(self, user_id):
        job = self.getjob(user_id)
        return self.getjobs(user_id)[job] / 100

    def getjobs(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT jobs FROM users WHERE user_id=?", t)
        return eval(c.fetchone()[0])

    def getjob(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT job FROM users WHERE user_id=?", t)
        return c.fetchone()[0]

    def changejob(self, user_id, job):
        c = conn.cursor()
        t = (job, user_id)
        c.execute("UPDATE users SET job=? WHERE user_id=?", t)
        conn.commit()

    def getdegree(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT degree FROM users WHERE user_id=?", t)
        return c.fetchone()[0]

    def changedegree(self, user_id, degree):
        c = conn.cursor()
        t = (degree, user_id)
        c.execute("UPDATE users SET degree=? WHERE user_id=?", t)
        conn.commit()

    def work(self, user_id, job, income):
        c = conn.cursor()
        balance = self.updatebal(user_id, income)
        t = (user_id,)
        c.execute("SELECT jobs FROM users WHERE user_id=?", t)
        jobs = eval(c.fetchone()[0])
        if job != "Unemployed": jobs[job] += 1
        t = (str(jobs), user_id)
        c.execute("UPDATE users SET jobs=? WHERE user_id=?", t)
        conn.commit()
        self.worked(user_id)
        return balance

    def study(self, user_id, debt):
        c = conn.cursor()
        debt = self.updatedebt(user_id, debt)
        t = (user_id,)
        c.execute("UPDATE users SET degreeprogress=degreeprogress+1 WHERE user_id=?", t)
        conn.commit()
        return (self.progress(user_id), debt)

    def progress(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT degreeprogress FROM users WHERE user_id=?", t)
        return c.fetchone()[0]

    def worked(self, user_id):
        c = conn.cursor()
        t = (time.time() / 60 + 60, user_id)
        c.execute("UPDATE users SET lastwork=? WHERE user_id=?", t)
        conn.commit()

    def studied(self, user_id):
        c = conn.cursor()
        t = (time.time() / 60 + 60, user_id)
        c.execute("UPDATE users SET laststudy=? WHERE user_id=?", t)
        conn.commit()

    def resign(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("UPDATE users SET job='Unemployed' WHERE user_id=?", t)
        conn.commit()

    def drop(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("UPDATE users SET degree='None', degreeprogress=0 WHERE user_id=?", t)
        conn.commit()

    def setbal(self, user_id, bal):
        c = conn.cursor()
        if bal < 0: bal = 0
        t = (bal, user_id)
        c.execute("UPDATE users SET fbux=? WHERE user_id=?", t)
        conn.commit()

    def updatebal(self, user_id, income):
        c = conn.cursor()
        t = (income, income, user_id)
        c.execute("UPDATE users SET fbux=fbux+?, netfbux=netfbux+? WHERE user_id=?", t)
        conn.commit()
        t = (user_id,)
        c.execute("SELECT fbux FROM users WHERE user_id=?", t)
        return c.fetchone()[0]

    def updatedebt(self, user_id, debt):
        c = conn.cursor()
        t = (debt, debt, user_id)
        c.execute("UPDATE users SET debt=debt+?, netdebt=netdebt+? WHERE user_id=?", t)
        conn.commit()
        t = (user_id,)
        c.execute("SELECT debt FROM users WHERE user_id=?", t)
        return c.fetchone()[0]

    def payoff(self, user_id, debt, loss):
        c = conn.cursor()
        t = (debt, loss, user_id)
        c.execute("UPDATE users SET debt=debt-?, fbux=fbux-? WHERE user_id=?", t)
        conn.commit()

    def finishdegree(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute("UPDATE users SET degree='None', degreeprogress=0 WHERE user_id=?", t)
        conn.commit()

    def startjob(self, user_id, job):
        c = conn.cursor()
        t = (user_id,)
        c.execute("SELECT jobs FROM users WHERE user_id=?", t)
        jobs = eval(c.fetchone()[0])
        jobs[job] = 100
        t = (str(jobs), user_id)
        c.execute("UPDATE users SET jobs=? WHERE user_id=?", t)
        conn.commit()

    def gettop(self, tt, amount, obj_id):
        tt = tt.replace("votes", "vote")
        tt = tt.replace("multis", "multi")
        tt = tt.replace("bal", "fbux")
        if tt == "vote":
            tt = "topvotes"
            ID, table = "user_id", "votes"
        elif tt == "counting":
            tt = "record"
            ID, table = "guild_id", "counter"
        elif tt == "multi":
            tt = "multiplier"
            ID, table = "user_id", "users"
        elif tt == "servmulti":
            tt = "multiplier"
            ID, table = "guild_id", "guilds"
        else:
            ID, table = "user_id", "users"
        c = conn.cursor()
        c.execute(f"SELECT {ID}, {tt} FROM {table} ORDER BY {tt} DESC LIMIT {amount}")
        top = enumerate(c)

        c = conn.cursor()
        c.execute(f"SELECT {ID}, {tt} FROM {table} ORDER BY {tt} DESC")
        for rank, row in enumerate(c):
            newobj_id, selftop = row
            if newobj_id == obj_id:
                break
        rank = str(rank+1)
        if rank.endswith("1") and not rank.endswith("11"): rank += "st"
        elif rank.endswith("2") and not rank.endswith("12"): rank += "nd"
        elif rank.endswith("3") and not rank.endswith("13"): rank += "rd"
        else: rank += "th"
        return (top, selftop, rank)

    def getinventory(self, user_id):
        c = conn.cursor()
        t = (user_id,)
        c.execute(f"SELECT inventory FROM users where user_id=?", t)
        return eval(c.fetchone()[0])

    def getitem(self, user_id, item):
        inv = self.getinventory(user_id)
        if item in inv:
            return inv[item]
        return 0

    def additem(self, user_id, item, amount):
        items = self.getitem(user_id, item)
        inv = self.getinventory(user_id)
        inv[item] = items + amount
        c = conn.cursor()
        t = (str(inv), user_id)
        c.execute(f"UPDATE users SET inventory=? WHERE user_id=?", t)
        conn.commit()

    def removeitem(self, user_id, item, amount):
        items = self.getitem(user_id, item)
        inv = self.getinventory(user_id)
        inv[item] = items - amount
        c = conn.cursor()
        t = (str(inv), user_id)
        c.execute(f"UPDATE users SET inventory=? WHERE user_id=?", t)
        conn.commit()

    # Voting

    def vote(self, user_id, site):
        c = conn.cursor()
        user_id = int(user_id)
        t = (user_id,)
        c.execute("SELECT user_id FROM votes WHERE user_id=?", t)
        if c.fetchone() is None:
            t = (user_id, 0, 0, 0, 0, 0, 0)
            marks = ",".join(["?"] * 7)
            c.execute(f"INSERT INTO votes VALUES({marks})", t)
            conn.commit()
        t = (user_id, )
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