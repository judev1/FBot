from datetime import datetime
import sqlite3

class db:

    def __init__(self):

        path = f"./Info/FBot.db"
        self.conn = sqlite3.connect(path)
        self.c = self.conn.cursor()
        
        self.c.execute("""CREATE TABLE IF NOT EXISTS guilds (
                          guild_id integer NOT NULL,
                          modtoggle string NOT NULL,
                          prefix string NOT NULL,
                          priority string NOT NULL,
                          multiplier integer NOT NULL
                          )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS channels (
                          guild_id integer NOT NULL,
                          channel_id integer NOT NULL,
                          status string NOT NULL
                          )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS users (
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
                          degreeprogress integer NOT NULL
                          )""")

        self.c.execute("""CREATE TABLE IF NOT EXISTS counter (
                          guild_id integer NOT NULL,
                          channel_id integer NOT NULL,
                          number integer NOT NULL,
                          user_id integer NOT NULL,
                          record integer NOT NULL
                          )""")
        
        self.conn.commit()
        print(" > Connected to FBot.db")

    def Check_Guilds(self, guilds):

        conn, c = self.conn, self.c
        discord_guild_ids = [guild.id for guild in guilds]

        for guild_id in discord_guild_ids:
            t = (guild_id,)
            try:
                c.execute(f"SELECT * FROM guilds where guild_id=?", t)
                c.fetchone()[0]
            except:
                self.Add_Guild(guild_id)

        count = 0
        c.execute(f"SELECT guild_id FROM guilds")
        for guild_id in c.fetchall():
            if not (guild_id[0] in discord_guild_ids):
                count += 1
                c.execute("DELETE FROM guilds WHERE guild_id=?", guild_id)
        print("Deleted", count, "guilds from 'guilds'")

        count = 0
        c.execute(f"SELECT guild_id FROM channels")
        for guild_id in c.fetchall():
            if not (guild_id[0] in discord_guild_ids):
                count += 1
                c.execute("DELETE FROM channels WHERE guild_id=?", guild_id)
        print("Deleted", count, "guild channels from 'channels'")

        count = 0
        c.execute(f"SELECT guild_id FROM counter")
        for guild_id in c.fetchall():
            if not (guild_id[0] in discord_guild_ids):
                count += 1
                c.execute("DELETE FROM counter WHERE guild_id=?", guild_id)
        print("Deleted", count, "guilds from 'counter'\n")
                
        conn.commit()

    # General

    def Add_Guild(self, guild_id):
        t = (guild_id,)
        self.c.execute("INSERT INTO guilds VALUES(?, 'off', 'fbot', 'all', 1000000);", t)
        self.c.execute("INSERT INTO counter VALUES(?, 0, 0, 0, 0)", t)
        self.conn.commit()

    def Remove_Guild(self, guild_id):
        t = (guild_id,)
        self.c.execute("DELETE FROM guilds WHERE guild_id=?;", t)
        self.c.execute("DELETE FROM channels WHERE guild_id=?;", t)
        self.c.execute("DELETE FROM counter WHERE guild_id=?", t)
        self.conn.commit()

    def Add_Channel(self, channel_id, guild_id):
        t = (guild_id, channel_id)
        try:
            self.c.execute("SELECT * FROM channels where channel_id=?", [t[1]])
            self.c.fetchone()[1]
        except:
            self.c.execute("INSERT INTO channels VALUES (?, ?, 'off')", t)
            self.conn.commit()

    # Status

    def Change_Modtoggle(self, guild_id, modtoggle):
        t = (modtoggle, guild_id)
        self.c.execute("UPDATE guilds SET modtoggle=? WHERE guild_id=?", t)
        self.conn.commit()

    def Get_Modtoggle(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT modtoggle FROM guilds WHERE guild_id=?", t)
        return self.c.fetchone()[0]

    def Change_Status(self, channel_id, status):
        t = (status, channel_id)
        self.c.execute("UPDATE channels SET status=? WHERE channel_id=?", t)
        self.conn.commit()

    def Get_Status(self, channel_id):
        t = (channel_id,)
        self.c.execute("SELECT status FROM channels WHERE channel_id=?", t)
        return self.c.fetchone()[0]

    def Get_All_Status(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT channel_id, status FROM channels WHERE guild_id=?", t)
        newdata = []
        for channel in self.c.fetchall():
            newdata.append((channel[0], channel[1]))
        return newdata


    # Economy

    def register(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT user_id FROM users WHERE user_id=?", t)
        if self.c.fetchone() is None:
            t = (user_id,-1,10000,0,0,0,0,'None', '{}', 'None',0,0,0)
            marks = ",".join(["?"] * 13)
            self.c.execute(f"INSERT INTO users VALUES({marks})", t)
            self.conn.commit()

    def increasemultiplier(self, user_id, guild_id, number):
        t = (number, user_id)
        self.c.execute("UPDATE users SET multiplier=multiplier+? WHERE user_id=?;", t)
        t = (number, guild_id)
        self.c.execute("UPDATE guilds SET multiplier=multiplier+? WHERE guild_id=?", t)
        self.conn.commit()

    def getprofile(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT fbux, netfbux, debt, netdebt, job, degree, degreeprogress FROM users WHERE user_id=?", t)
        return self.c.fetchone()

    def getbal(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT fbux FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def getmultis(self, user_id, guild_id):
        t = (user_id,)
        self.c.execute("SELECT multiplier FROM users WHERE user_id=?", t)
        usermulti = round(self.c.fetchone()[0]/(10**4), 2)
        t = (guild_id,)
        self.c.execute("SELECT multiplier FROM guilds WHERE guild_id=?", t)
        guildmulti = round(self.c.fetchone()[0]/(10**6), 2)
        return (usermulti, guildmulti)

    def getusermulti(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT multiplier FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def getjobs(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT jobs FROM users WHERE user_id=?", t)
        return eval(self.c.fetchone()[0])

    def getjob(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT job FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def changejob(self, user_id, job):
        t = (user_id,)
        self.c.execute("SELECT degree FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def getdegree(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT degree FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def changedegree(self, user_id, degree):
        t = (degree, user_id)
        self.c.execute("UPDATE users SET degree=? WHERE user_id=?", t)
        self.conn.commit()

    def work(self, user_id, job, income):
        balance = self.updatebal(user_id, income)
        t = (user_id,)
        self.c.execute("SELECT jobs FROM users WHERE user_id=?", t)
        jobs = eval(self.c.fetchone()[0])
        if job != "Unemployed": jobs[job] += 1
        t = (str(jobs), user_id)
        self.c.execute("UPDATE users SET jobs=? WHERE user_id=?", t)
        self.conn.commit()
        self.worked(user_id)
        return balance

    def study(self, user_id):
        t = (user_id,)
        self.c.execute("UPDATE users SET degreeprogress=degreeprogress+1 WHERE user_id=?", t)
        self.conn.commit()
        t = (user_id,)
        self.c.execute("SELECT degreeprogress FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def canwork(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT lastwork FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0] <= datetime.now().timestamp() / 60

    def canstudy(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT laststudy FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0] <= datetime.now().timestamp() / 60

    def lastwork(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT lastwork FROM users WHERE user_id=?", t)
        return round(self.c.fetchone()[0] - datetime.now().timestamp() / 60)

    def laststudy(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT laststudy FROM users WHERE user_id=?", t)
        return round(self.c.fetchone()[0] - datetime.now().timestamp() / 60)

    def worked(self, user_id):
        t = (datetime.now().timestamp() / 60 + 60, user_id)
        self.c.execute("UPDATE users SET lastwork=? WHERE user_id=?", t)
        self.conn.commit()

    def studied(self, user_id):
        t = (datetime.now().timestamp() / 60 + 60, user_id)
        self.c.execute("UPDATE users SET laststudy=? WHERE user_id=?", t)
        self.conn.commit()

    def updatebal(self, user_id, income):
        t = (income, income, user_id)
        self.c.execute("UPDATE users SET fbux=fbux+?, netfbux=netfbux+? WHERE user_id=?", t)
        self.conn.commit()
        t = (user_id,)
        self.c.execute("SELECT fbux FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def finishdegree(self, user_id):
        t = (user_id,)
        self.c.execute("UPDATE users SET degree='None', degreeprogress=0 WHERE user_id=?", t)
        self.conn.commit()

    def startjob(self, user_id, job):
        t = (user_id,)
        self.c.execute("SELECT jobs FROM users WHERE user_id=?", t)
        jobs = eval(self.c.fetchone()[0])
        jobs[job] = 100
        t = (str(jobs), user_id)
        self.c.execute("UPDATE users SET jobs=? WHERE user_id=?", t)
        self.conn.commit()
        

    # Prefix

    def Change_Prefix(self, guild_id, prefix):
        t = (prefix, guild_id)
        self.c.execute("UPDATE guilds SET prefix=? WHERE guild_id=?", t)
        self.conn.commit()

    def Get_Prefix(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT prefix FROM guilds WHERE guild_id=?", t)
        return self.c.fetchone()[0]

    def Change_Priority(self, guild_id, priority):
        t = (priority, guild_id)
        self.c.execute("UPDATE guilds SET priority=? WHERE guild_id=?", t)
        self.conn.commit()

    def Get_Priority(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT priority FROM guilds WHERE guild_id=?", t)
        return self.c.fetchone()[0]

    # ppsize

    def getppsize(self, user_id):
        t = (user_id,)
        self.c.execute("SELECT ppsize FROM users WHERE user_id=?", t)
        return self.c.fetchone()[0]

    def updateppsize(self, user_id, size):
        t = (size, user_id)
        self.c.execute("UPDATE users SET ppsize=? WHERE user_id=?", t)
        self.conn.commit()

    # Counting
        
    def ignorechannel(self, guild_id, channel_id):
        t = (guild_id,)
        self.c.execute("SELECT channel_id FROM counter WHERE guild_id=?", t)
        if channel_id != self.c.fetchone()[0]: return True
        return False

    def checkdouble(self, guild_id, user_id):
        t = (guild_id,)
        self.c.execute("SELECT user_id FROM counter WHERE guild_id=?", t)
        if user_id == self.c.fetchone()[0]:
            t = (guild_id,)
            self.c.execute("UPDATE counter SET number=0, user_id=0 WHERE guild_id=?", t)
            self.conn.commit()
            return True
        return False

    def getnumber(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT number FROM counter WHERE guild_id=?", t)
        return int(self.c.fetchone()[0])

    def getuser(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT user_id FROM counter WHERE guild_id=?", t)
        return int(self.c.fetchone()[0])

    def gethighscore(self, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT record FROM counter WHERE guild_id=?", t)
        return self.c.fetchone()[0]

    def gethighscores(self):
        self.c.execute("SELECT guild_id, record FROM counter ORDER BY record DESC LIMIT 5")
        return self.c.fetchall()

    def resetnumber(self, guild_id):
        t = (guild_id,)
        self.c.execute("UPDATE counter SET number=0, user_id=0 WHERE guild_id=?", t)
        self.conn.commit()

    def updatenumber(self, number, author_id, guild_id):
        t = (number, author_id, guild_id,)
        self.c.execute("UPDATE counter SET number=?, user_id=? WHERE guild_id=?", t)
        self.conn.commit()

    def highscore(self, number, guild_id):
        t = (guild_id,)
        self.c.execute("SELECT record FROM counter WHERE guild_id=?", t)
        if number > self.c.fetchone()[0]:
            t = (number, guild_id,)
            self.c.execute("UPDATE counter SET record=? WHERE guild_id=?", t)
            self.conn.commit()
        
    def setcountingchannel(self, channel_id, guild_id):	
        t = (channel_id, guild_id)	
        self.c.execute("UPDATE counter SET channel_id=? WHERE guild_id=?", t)	
        self.conn.commit()
