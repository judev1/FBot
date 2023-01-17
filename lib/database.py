from datetime import datetime
import sqlite3
import time
import os

def setup():
    global conn
    path = "./data/FBot.db"
    conn = sqlite3.connect(path)

    with open(path, "rb") as file:
        filename = datetime.now().strftime("%y-%m-%d %H%M")
        if not os.path.exists(os.path.join("data", "db_backups")):
            os.makedirs(os.path.join("data", "db_backups"))
        with open(f"./data/db_backups/{filename}.db", "wb+") as newfile:
            newfile.writelines(file.readlines())

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS guilds (
                        guild_id integer NOT NULL,
                        notice string NOT NULL,

                        prefix string NOT NULL,
                        modtoggle string NOT NULL,
                        priority string NOT NULL,
                        mode string NOT NULL,
                        language string NOT NULL,

                        name string NOT NULL,
                        picture string NOT NULL,
                        triggers string NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS channels (
                        guild_id integer NOT NULL,
                        channel_id integer NOT NULL,
                        status string NOT NULL,

                        shout string NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_id integer NOT NULL,
                        ppsize integer NOT NULL,

                        commands integer NOT NULL,
                        triggers integer NOT NULL,

                        title string NOT NULL,
                        colour integer NOT NULL,
                        emoji string NOT NULL,
                        say string NOT NULL,
                        delete_say string NOT NULL,
                        claims integer NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS claims (
                        guild_id integer NOT NULL,
                        channel_id integer NOT NULL,
                        expiry integer NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS notices (
                        date integer NOT NULL,
                        title string NOT NULL,
                        message string NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS counting (
                        guild_id integer NOT NULL,
                        channel_id integer NOT NULL,
                        number integer NOT NULL,
                        user_id integer NOT NULL,
                        record integer NOT NULL
                    );""")

    c.execute("""CREATE TABLE IF NOT EXISTS votes (
                        user_id integer NOT NULL,
                        topvotes integer NOT NULL,
                        dblvotes integer NOT NULL,
                        bfdvotes integer NOT NULL,
                        total_topvotes integer NOT NULL,
                        total_dblvotes integer NOT NULL,
                        total_bfdvotes integer NOT NULL,
                        last_topvote integer NOT NULL,
                        last_dblvote integer NOT NULL,
                        last_bfdvote integer NOT NULL
                    );""")

    conn.commit()

def checkguilds(guilds):
    c = conn.cursor()
    guild_ids = dict()
    for guild in guilds:
        guild_ids[guild.id] = guild

    for i, guild_id in enumerate(guild_ids):
        t = (guild_id,)
        c.execute("SELECT * FROM guilds where guild_id=?;", t)
        if not c.fetchone():
            addguild(guild_id)

    count = [0, 0]
    c.execute("SELECT guild_id FROM guilds;")
    for i, guild_id in enumerate(c.fetchall()):
        if not (guild_id[0] in guild_ids):
            count[0] += 1
            c.execute("DELETE FROM guilds WHERE guild_id=?;", guild_id)
            # Deliberately not deleting channels or counting
        else:
            channel_ids = [channel.id for channel in guild_ids[guild_id[0]].channels]
            c.execute("SELECT channel_id FROM channels WHERE guild_id=?;", guild_id)
            channels = c.fetchall()
            for channel_id in channels:
                if not (channel_id[0] in channel_ids):
                    count[1] += 1
                    c.execute("DELETE FROM channels WHERE channel_id=?;", channel_id)

    print("Removed", count[0], "guilds from 'guilds'")
    print("Removed", count[1], "channels from 'channels'")

    count = 0
    c.execute("SELECT guild_id FROM channels;")
    for guild_id in c.fetchall():
        if not (guild_id[0] in guild_ids):
            count += 1
            c.execute("DELETE FROM channels WHERE guild_id=?;", guild_id)
    print("Removed", count, "guild channels from 'channels'")

    count = 0
    c.execute("SELECT guild_id FROM counting;")
    for guild_id in c.fetchall():
        if not (guild_id[0] in guild_ids):
            count += 1
            c.execute("DELETE FROM counting WHERE guild_id=?;", guild_id)
    print("Removed", count, "guilds from 'counting'\n")

    conn.commit()

# General

def addguild(guild_id):
    c = conn.cursor()
    t = (guild_id, time.time())
    c.execute("""INSERT INTO guilds (
                        guild_id, notice,
                        prefix, modtoggle, priority, mode, language,
                        name, picture, triggers
                    )
                    VALUES (
                        ?, ?,
                        'fbot', 'off', 'all', 'default', 'english',
                        '', '', '{}'
                    );""", t)
    t = (guild_id,)
    c.execute("""INSERT INTO counting (
                        guild_id, channel_id, number, user_id, record
                    )
                    VALUES (
                        ?, 0, 0, 0, 0
                    );""", t)
    conn.commit()

def removeguild(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("DELETE FROM guilds WHERE guild_id=?;", t)
    c.execute("DELETE FROM channels WHERE guild_id=?;", t)
    c.execute("DELETE FROM counting WHERE guild_id=?;", t)
    conn.commit()

def addchannel(channel_id, guild_id):
    c = conn.cursor()
    t = (channel_id,)
    c.execute("SELECT * FROM channels where channel_id=?;", t)
    if not c.fetchone():
        t = (guild_id, channel_id)
        c.execute("""INSERT INTO channels (
                        guild_id, channel_id, status,
                        shout
                    )
                    VALUES (
                        ?, ?, 'off',
                        'no'
                    );""", t)
        conn.commit()

# Config

def changemodtoggle(guild_id, modtoggle):
    c = conn.cursor()
    t = (modtoggle, guild_id)
    c.execute("UPDATE guilds SET modtoggle=? WHERE guild_id=?;", t)
    conn.commit()

def getmodtoggle(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT modtoggle FROM guilds WHERE guild_id=?;", t)
    return c.fetchone()[0]

def changemode(guild_id, mode):
    c = conn.cursor()
    t = (mode, guild_id)
    c.execute("UPDATE guilds SET mode=? WHERE guild_id=?;", t)
    conn.commit()

def getmode(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT mode FROM guilds WHERE guild_id=?;", t)
    return c.fetchone()[0]

def getlang(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT language FROM guilds WHERE guild_id=?;", t)
    return c.fetchone()[0]

def changestatus(channel_id, status):
    c = conn.cursor()
    t = (status, channel_id)
    c.execute("UPDATE channels SET status=? WHERE channel_id=?;", t)
    conn.commit()

def getstatus(channel_id):
    c = conn.cursor()
    t = (channel_id,)
    c.execute("SELECT status FROM channels WHERE channel_id=?;", t)
    return c.fetchone()[0]

def getallstatus(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT channel_id, status FROM channels WHERE guild_id=?;", t)
    newdata = []
    for channel in c.fetchall():
        newdata.append((channel[0], channel[1]))
    return newdata

# Notices

def addnotice(date, title, message):
    c = conn.cursor()
    t = (date, title, message)
    c.execute("""INSERT INTO notices (
                    date, title, message
                )
                VALUES (
                    ?, ?, ?
                );""", t)
    conn.commit()

def editnotice(title, message):
    c = conn.cursor()
    t = (title, message, getlastnotice()[0])
    c.execute(f"UPDATE notices SET title=?, message=? WHERE date=?;", t)
    return c.fetchone()

def getlastnotice():
    c = conn.cursor()
    c.execute(f"SELECT * FROM notices ORDER BY date DESC LIMIT 1;")
    return c.fetchone()

def getservernotice(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute(f"SELECT notice FROM guilds WHERE guild_id=?;", t)
    return c.fetchone()[0]

def updateservernotice(guild_id):
    c = conn.cursor()
    t = (time.time(), guild_id)
    c.execute(f"UPDATE guilds SET notice=? WHERE guild_id=?;", t)
    conn.commit()

# Users

def register(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute("SELECT user_id FROM users WHERE user_id=?;", t)
    if c.fetchone() is None:
        c.execute(f"""INSERT INTO users (
                        user_id, ppsize,
                        commands, triggers,
                        title, colour, emoji, say, delete_say, claims
                    )
                    VALUES (
                        ?, -1,
                        0, 0,
                        '', {0xf42f42}, '', 'fbot', 'yes', 0
                    );""", t)
        conn.commit()

def gettop(toptype, amount, obj_id):

    if toptype == "votes":
        TABLE, DATA, ID = "votes", "total_topvotes, total_bfdvotes, total_dblvotes", "user_id"
    elif toptype == "counting":
        TABLE, DATA, ID = "counting", "record", "guild_id"
    if toptype == "votes":
        ORDER = "total_topvotes + total_bfdvotes + total_dblvotes"
    else:
        ORDER = DATA

    c = conn.cursor()
    c.execute(f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC LIMIT {amount};")
    top = c.fetchall()

    if toptype == "votes":
        newtop = []
        for data in top:
            if toptype == "votes":
                item = sum(data[1:])
            newtop.append([data[0], item])
        top = newtop

    score = 0
    rank = 0
    if obj_id != -1:
        c.execute(f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC;")
        for rank, data in enumerate(c):
            if data[0] == obj_id:
                score = sum(data[1:])
                break

    return (top, score, rank + 1)

# Voting

def addvoter(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute("SELECT user_id FROM votes WHERE user_id=?;", t)
    if not c.fetchone():
        c.execute("""INSERT INTO votes (
                        user_id,
                        topvotes, dblvotes, bfdvotes,
                        total_topvotes, total_dblvotes, total_bfdvotes,
                            last_topvote, last_dblvote, last_bfdvote
                    )
                    VALUES (
                        ?,
                        0, 0, 0,
                        0, 0, 0,
                        0, 0, 0
                    );""", t)
        conn.commit()

def vote(user_id, site):
    user_id = int(user_id)
    addvoter(user_id)

    c = conn.cursor()
    t = (user_id,)
    c.execute(f"UPDATE votes SET {site}votes={site}votes+1, "
                f"total_{site}votes=total_{site}votes+1, "
                f"last_{site}vote={time.time()} WHERE user_id=?;", t)

    conn.commit()

def nextvote(user_id, site):
    c = conn.cursor()
    user_id = int(user_id)
    t = (user_id,)
    c.execute(f"SELECT last_{site}vote FROM votes where user_id=?;", t)
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

# Prefix

def changeprefix(guild_id, prefix):
    c = conn.cursor()
    t = (prefix, guild_id)
    c.execute("UPDATE guilds SET prefix=? WHERE guild_id=?;", t)
    conn.commit()

def getprefix(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT prefix FROM guilds WHERE guild_id=?;", t)
    return c.fetchone()[0]

def changepriority(guild_id, priority):
    c = conn.cursor()
    t = (priority, guild_id)
    c.execute("UPDATE guilds SET priority=? WHERE guild_id=?;", t)
    conn.commit()

def getpriority(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT priority FROM guilds WHERE guild_id=?;", t)
    return c.fetchone()[0]

# ppsize

def getppsize(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute("SELECT ppsize FROM users WHERE user_id=?;", t)
    return c.fetchone()[0]

def updateppsize(user_id, size):
    c = conn.cursor()
    t = (size, user_id)
    c.execute("UPDATE users SET ppsize=? WHERE user_id=?;", t)
    conn.commit()

# Stats

def usecommand(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute("UPDATE users SET commands=commands+1 WHERE user_id=?;", t)
    conn.commit()

def usetrigger(user_id):
    c = conn.cursor()
    t = (user_id,)
    c.execute("UPDATE users SET triggers=triggers+1 WHERE user_id=?;", t)
    conn.commit()

# Counting

def checkdouble(guild_id, user_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT user_id FROM counting WHERE guild_id=?;", t)
    if user_id == c.fetchone()[0]:
        t = (guild_id,)
        c.execute("UPDATE counting SET number=0, user_id=0 WHERE guild_id=?;", t)
        conn.commit()
        return True
    return False

def getnumber(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT number FROM counting WHERE guild_id=?;", t)
    return int(c.fetchone()[0])

def getuser(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT user_id FROM counting WHERE guild_id=?;", t)
    return int(c.fetchone()[0])

def resetnumber(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("UPDATE counting SET number=0, user_id=0 WHERE guild_id=?;", t)
    conn.commit()

def updatenumber(number, author_id, guild_id):
    c = conn.cursor()
    t = (number, author_id, guild_id,)
    c.execute("UPDATE counting SET number=?, user_id=? WHERE guild_id=?;", t)

    t = (guild_id,)
    c.execute("SELECT record FROM counting WHERE guild_id=?;", t)
    if number > c.fetchone()[0]:
        t = (number, guild_id,)
        c.execute("UPDATE counting SET record=? WHERE guild_id=?;", t)
        conn.commit()

def gethighscore(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT record FROM counting WHERE guild_id=?;", t)
    return c.fetchone()[0]

def gethighscores(self):
    c = conn.cursor()
    c.execute("SELECT guild_id, record FROM counting ORDER BY record DESC LIMIT 5;")
    return c.fetchall()

def setcountingchannel(channel_id, guild_id):
    c = conn.cursor()
    t = (channel_id, guild_id)
    c.execute("UPDATE counting SET channel_id=? WHERE guild_id=?;", t)
    conn.commit()

def removecountingchannel(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("UPDATE counting SET channel_id=0 WHERE guild_id=?;", t)
    conn.commit()

def getcountingchannel(guild_id):
    c = conn.cursor()
    t = (guild_id,)
    c.execute("SELECT channel_id FROM counting WHERE guild_id=?;", t)
    return c.fetchone()[0]