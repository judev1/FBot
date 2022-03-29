from datetime import datetime
import sqlite3
import time
import os

def fetchone(query, t=tuple()):
    c = conn.cursor()
    c.execute(query + ";", t)
    result = c.fetchone()
    if result:
        if len(result) == 1:
            return result[0]
    return result

def fetchall(query, t=tuple()):
    c = conn.cursor()
    c.execute(query + ";", t)
    return c.fetchall()

def update(query, t=tuple()):
    conn.cursor().execute(query + ";", t)
    conn.commit()

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

    update("""
        CREATE TABLE IF NOT EXISTS guilds (
            guild_id integer NOT NULL,
            notice string NOT NULL,

            prefix string NOT NULL,
            modtoggle string NOT NULL,
            priority string NOT NULL,
            mode string NOT NULL,
            language string NOT NULL,

            name string NOT NULL,
            picture string NOT NULL,

            custom_commands string NOT NULL,
            commands integer NOT NULL,
            triggers integer NOT NULL,
            joined integer NOT NULL,
            removed integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS channels (
            guild_id integer NOT NULL,
            channel_id integer NOT NULL,
            status string NOT NULL,

            shout string NOT NULL
        )""")

    # Keeping commands and triggers for backwards compatibility
    update("""
        CREATE TABLE IF NOT EXISTS users (
            user_id integer NOT NULL,
            ppsize integer NOT NULL,

            commands integer NOT NULL,
            triggers integer NOT NULL,

            expiry integer NOT NULL,
            title string NOT NULL,
            colour integer NOT NULL,
            emoji string NOT NULL,
            say string NOT NULL,
            delete_say string NOT NULL,
            claims integer NOT NULL,
            custom_triggers integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS interactions (
            user_id integer NOT NULL,
            guild_id integer NOT NULL,
            type string NOT NULL,
            name string NOT NULL,
            sent integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS claims (
            guild_id integer NOT NULL,
            channel_id integer NOT NULL,
            expiry integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS custom_commands (
            trigger_id integer PRIMARY KEY AUTOINCREMENT,
            user_id integer NOT NULL,
            message string NOT NULL,
            type string NOT NULL,
            'case' string NOT NULL,
            response string NOT NULL,
            priority string NOT NULL,
            public string NOT NULL,
            uses integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS notices (
            date integer NOT NULL,
            title string NOT NULL,
            message string NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS counting (
            guild_id integer NOT NULL,
            channel_id integer NOT NULL,
            number integer NOT NULL,
            user_id integer NOT NULL,
            record integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS topvotes (
            user_id integer NOT NULL,
            votes integer NOT NULL,
            total_votes integer NOT NULL,
            last_vote integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS dblvotes (
            user_id integer NOT NULL,
            votes integer NOT NULL,
            total_votes integer NOT NULL,
            last_vote integer NOT NULL
        )""")

    update("""
        CREATE TABLE IF NOT EXISTS bfdvotes (
            user_id integer NOT NULL,
            votes integer NOT NULL,
            total_votes integer NOT NULL,
            last_vote integer NOT NULL
        )""")

def checkguilds(guilds):

    guild_ids = dict()
    for guild in guilds:
        guild_ids[guild.id] = guild

    query = "SELECT * FROM guilds where guild_id=?"
    for guild_id in guild_ids:
        if not fetchone(query, (guild_id,)):
            addguild(guild_id)

    count = 0
    for guild_id in fetchall("SELECT guild_id FROM guilds"):
        guild_id = guild_id[0]
        if guild_id in guild_ids:
            channels = guild_ids[guild_id].channels
            channel_ids = [channel.id for channel in channels]
            query = "SELECT channel_id FROM channels WHERE guild_id=?"
            for channel_id in fetchall(query, (guild_id,)):
                if not (channel_id[0] in channel_ids):
                    count[1] += 1
                    query = "DELETE FROM channels WHERE channel_id=?"
                    update(query, (channel_id,))
    print("Removed", count, "channels from 'channels'")

    count = 0
    for guild_id in fetchall("SELECT guild_id FROM channels"):
        if not (guild_id[0] in guild_ids):
            count += 1
            query = "DELETE FROM channels WHERE guild_id=?"
            update(query, (guild_id,))
    print("Removed", count, "guild channels from 'channels'\n")


# General

def addguild(guild_id):
    update("""
        INSERT INTO guilds (
            guild_id, notice,
            prefix, modtoggle, priority, mode, language,
            name, picture, custom_commands,
            commands, triggers, joined, removed
        )
        VALUES (
            ?, ?,
            'fbot', 'off', 'all', 'default', 'english',
            '', '', '[]',
            0, 0, ?, 0
        )""", (guild_id, time.time(), time.time()))
    update("""
        INSERT INTO counting (
            guild_id, channel_id, number, user_id, record
        ) VALUES (
            ?, 0, 0, 0, 0
        )""", (guild_id,))

def removeguild(guild_id):
    query = "UPDATE guilds SET removed=? WHERE guild_id=?"
    update(query, (time.time(), guild_id))

def addchannel(channel_id, guild_id):
    query = "SELECT * FROM channels where channel_id=?"
    if not fetchone(query, (channel_id,)):
        update("""
            INSERT INTO channels (
                guild_id, channel_id, status, shout
            ) VALUES (
                ?, ?, 'off', 'no'
            )""", (guild_id, channel_id,))


# Config

def getmodtoggle(guild_id):
    query = "SELECT modtoggle FROM guilds WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def setmodtoggle(guild_id, modtoggle):
    query = "UPDATE guilds SET modtoggle=? WHERE guild_id=?"
    update(query, (modtoggle, guild_id))

def getmode(guild_id):
    query = "SELECT mode FROM guilds WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def setmode(guild_id, mode):
    query = "UPDATE guilds SET mode=? WHERE guild_id=?"
    update(query, (mode, guild_id))

def getlang(guild_id):
    query = "SELECT language FROM guilds WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def getstatus(channel_id):
    query = "SELECT status FROM channels WHERE channel_id=?"
    return fetchone(query, (channel_id,))

def getallstatus(guild_id):
    newdata = list()
    query = "SELECT channel_id, status FROM channels WHERE guild_id=?"
    for channel in fetchall(query, (guild_id,)):
        newdata.append((channel[0], channel[1]))
    return newdata

def setstatus(channel_id, status):
    query = "UPDATE channels SET status=? WHERE channel_id=?"
    update(query, (status, channel_id))


# Notices

def addnotice(date, title, message):
    update("""
        INSERT INTO notices (
            date, title, message
        ) VALUES (
            ?, ?, ?
        )""", (date, title, message)
    )

def getnotice():
    query = f"SELECT * FROM notices ORDER BY date DESC LIMIT 1"
    return fetchone(query)

def setnotice(title, message):
    query = f"UPDATE notices SET title=?, message=? WHERE date=?"
    update(query, (title, message, getnotice()[0]))

def getservernotice(guild_id):
    query = f"SELECT notice FROM guilds WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def setservernotice(guild_id):
    query = f"UPDATE guilds SET notice=? WHERE guild_id=?"
    update(query, (time.time(), guild_id))


# Users

def register(user_id):
    query = "SELECT user_id FROM users WHERE user_id=?"
    if fetchone(query, (user_id,)) is None:
        update(f"""
            INSERT INTO users (
                user_id, ppsize, commands, triggers,
                expiry, title, colour, emoji, say, delete_say,
                claims, custom_triggers
            ) VALUES (
                ?, -1, 0, 0,
                0, '', {0xf42f42}, '', 'fbot', 'no', 0, 0
            )
        """, (user_id,)
    )

# comon jude rewrite this properly
def gettop(toptype, amount, obj_id):

    if toptype == "votes":
        TABLE, DATA, ID = "votes", "total_topvotes, total_bfdvotes, total_dblvotes", "user_id"
    elif toptype == "counting":
        TABLE, DATA, ID = "counting", "record", "guild_id"
    if toptype == "votes":
        ORDER = "total_topvotes + total_bfdvotes + total_dblvotes"
    else:
        ORDER = DATA

    query = f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC LIMIT {amount}"
    top = fetchall(query)

    if toptype == "votes":
        newtop = list()
        for data in top:
            if toptype == "votes":
                item = sum(data[1:])
            newtop.append([data[0], item])
        top = newtop

    score = 0
    rank = 0
    if obj_id != -1:
        query = f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC"
        for rank, data in enumerate(fetchall(query)):
            if data[0] == obj_id:
                score = sum(data[1:])
                break

    return (top, score, rank + 1)


# Voting

def addvoter(user_id, site):
    query = f"SELECT user_id FROM {site}votes WHERE user_id=?"
    if not fetchone(query, (user_id,)):
        update(f"""
            INSERT INTO {site}votes (
                user_id, votes, total_votes, last_bfdvote
            ) VALUES (
                ?, 0, 0, 0
            )
        """, (user_id,)
    )

def vote(user_id, site):
    addvoter(user_id, site)
    update(f"""
        UPDATE votes SET {site}votes={site}votes+1,
        total_{site}votes=total_{site}votes+1,
        last_{site}vote={time.time()} WHERE user_id=?
    """, (user_id,))

def nextvote(user_id, site):
    query = f"SELECT last_vote FROM {site}votes where user_id=?"
    lastvote = fetchone(query, (user_id,))

    if not lastvote:
        return None

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

def ispremium(user_id):
    query = "SELECT user_id FROM users WHERE user_id=?"
    return bool(fetchone(query, (user_id,)))

def getallpremium():
    query = "SELECT user_id, expiry FROM users WHERE expiry>?"
    return fetchall(query, (time.time(),))

def addpremium(user_id, expiry):
    query = "UPDATE users SET expiry=? WHERE user_id=?"
    update(query, (expiry, user_id))

def gettitle(user_id):
    query = "SELECT title FROM users WHERE user_id=?"
    return fetchone(query, (user_id,))

def settitle(user_id, title):
    query = "UPDATE users SET title=? WHERE user_id=?"
    update(query, (title, user_id))

def getcolour(user_id):
    query = "SELECT colour FROM users WHERE user_id=?"
    return fetchone(query, (user_id,))

def setcolour(user_id, colour):
    query = "UPDATE users SET colour=? WHERE user_id=?"
    update(query, (colour, user_id))

def getemoji(user_id):
    query = "SELECT emoji FROM users WHERE user_id=?"
    return fetchone(query, (user_id,))

def setemoji(user_id, emoji):
    query = "UPDATE users SET emoji=? WHERE user_id=?"
    update(query, (emoji, user_id))


# Prefix

def getprefix(guild_id):
    query = "SELECT prefix FROM guilds WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def setprefix(guild_id, prefix):
    query = "UPDATE guilds SET prefix=? WHERE guild_id=?"
    update(query, (prefix, guild_id))

def getpriority(guild_id):
    query = "SELECT priority FROM guilds WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def setpriority(guild_id, priority):
    query = "UPDATE guilds SET priority=? WHERE guild_id=?"
    update(query, (priority, guild_id))


# ppsize

def getppsize(user_id):
    query = "SELECT ppsize FROM users WHERE user_id=?"
    return fetchone(query, (user_id,))

def setppsize(user_id, size):
    query = "UPDATE users SET ppsize=? WHERE user_id=?"
    update(query, (size, user_id))


# Stats

def usecommand(user_id):
    query = "UPDATE users SET commands=commands+1 WHERE user_id=?"
    update(query, (user_id,))

def usetrigger(user_id):
    query = "UPDATE users SET triggers=triggers+1 WHERE user_id=?"
    update(query, (user_id,))


# Counting

def getnumber(guild_id):
    query = "SELECT number FROM counting WHERE guild_id=?"
    return int(fetchone(query, (guild_id,)))

def getuser(guild_id):
    query = "SELECT user_id FROM counting WHERE guild_id=?"
    return int(fetchone(query, (guild_id,)))

def setnumber(number, author_id, guild_id):
    query = "UPDATE counting SET number=?, user_id=? WHERE guild_id=?"
    update(query, (number, author_id, guild_id,))

    query = "SELECT record FROM counting WHERE guild_id=?"
    if number > fetchone(query, (guild_id,)):
        query = "UPDATE counting SET record=? WHERE guild_id=?"
        update(query, (number, guild_id,))

def resetnumber(guild_id):
    query = "UPDATE counting SET number=0, user_id=0 WHERE guild_id=?"
    update(query, (guild_id,))

def gethighscore(guild_id):
    query = "SELECT record FROM counting WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def getcountingchannel(guild_id):
    query = "SELECT channel_id FROM counting WHERE guild_id=?"
    return fetchone(query, (guild_id,))

def setcountingchannel(channel_id, guild_id):
    query = "UPDATE counting SET channel_id=? WHERE guild_id=?"
    update(query, (channel_id, guild_id))

def removecountingchannel(guild_id):
    query = "UPDATE counting SET channel_id=0 WHERE guild_id=?"
    update(query, (guild_id,))