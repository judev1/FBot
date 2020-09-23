import os
import sqlite3

path = f"./Info/FBot.db"

# Formats modtoggle and FBot status
def Val(value):
    if value == 0: return "off"
    elif value == 1: return "on"
    elif value == "off": return 0
    elif value == "on": return 1

class db():

    def Setup():        
        try:
            with open(path, "r") as file: pass
        except:
            with open(path, "w+") as file: pass

        global conn, c
        conn = sqlite3.connect(path)
        c = conn.cursor()
        
        c.execute("""CREATE TABLE IF NOT EXISTS guilds (
                    guild_id integer NOT NULL,
                    modtoggle integer NOT NULL,
                    prefix string NOT NULL,
                    priority string NOT NULL
                    )""")

        c.execute("""CREATE TABLE IF NOT EXISTS channels (
                    guild_id integer NOT NULL,
                    channel_id integer NOT NULL,
                    status integer NOT NULL
                    )""")

        c.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_id integer NOT NULL,
                    credits integer NOT NULL
                    )""")

        c.execute("""CREATE TABLE IF NOT EXISTS counter (
            guild_id integer NOT NULL,
            channel_id integer NOT NULL,
            number integer NOT NULL,
            user_id integer NOT NULL,
            record integer NOT NULL
            )""")
        
        conn.commit()
        print(" > Connected to FBot.db")

    def Check_Guilds(guilds):
        for guild in guilds:
            guild_id = guild.id
            t = (guild_id, )
            try:
                c.execute(f"SELECT * FROM guilds where guild_id == {guild_id};")
                c.fetchone()[0]
            except:
                c.execute(f"INSERT INTO guilds VALUES ({guild_id}, 0, 'fbot', 'all')")
                conn.commit()
            try:
                c.execute(f"SELECT * FROM counter where guild_id == {guild_id};")
                c.fetchone()[0]
            except:
                c.execute("INSERT INTO counter VALUES(?, 0, 0, 0, 0)", t)
                conn.commit()

    def Add_Guild(guild_id):
        c.execute(f"INSERT INTO guilds VALUES ({guild_id}, 0, 'fbot', 3)")
        conn.commit()

    def Remove_Guild(guild_id):
        c.execute(f"DELETE FROM guilds WHERE guild_id == {guild_id};")
        c.execute(f"DELETE FROM channels WHERE guild_id == {guild_id};")
        conn.commit()

    def Add_Channel(channel_id, guild_id):
        try:
            c.execute(f"SELECT * FROM channels where channel_id == {channel_id};")
            c.fetchone()[1]
        except:
            c.execute(f"INSERT INTO channels VALUES ({guild_id}, {channel_id}, 0)")
            conn.commit()

    def Change_Modtoggle(guild_id, modtoggle):
        c.execute(f"UPDATE guilds SET modtoggle = {Val(modtoggle)} WHERE guild_id == {guild_id};")
        conn.commit()

    def Get_Modtoggle(guild_id):
        c.execute(f"SELECT modtoggle FROM guilds WHERE guild_id == {guild_id};")
        modtoggle = Val(c.fetchone()[0])
        return modtoggle

    def Change_Status(channel_id, status):
        c.execute(f"UPDATE channels SET status = {Val(status)} WHERE channel_id = {channel_id};")
        conn.commit()

    def Get_Status(channel_id):
        c.execute(f"SELECT status FROM channels WHERE channel_id == {channel_id};")
        status = Val(c.fetchone()[0])
        return status

    def Change_Prefix(guild_id, prefix):
        if all(x.isalpha() or x.isspace() or x == "!" for x in prefix):
            c.execute(f"UPDATE guilds SET prefix = '{prefix}' WHERE guild_id == {guild_id}")
            conn.commit()

    def Get_Prefix(guild_id):
        c.execute(f"SELECT prefix FROM guilds WHERE guild_id == {guild_id};")
        prefix = c.fetchone()[0]
        return prefix

    def Change_Priority(guild_id, priority):
        c.execute(f"UPDATE guilds SET priority = '{priority}' WHERE guild_id == {guild_id}")
        conn.commit()

    def Get_Priority(guild_id):
        c.execute(f"SELECT priority FROM guilds WHERE guild_id == {guild_id};")
        priority = c.fetchone()[0]
        return priority

    def Get_All_Status(guild_id):
        c.execute(f"SELECT channel_id, status FROM channels WHERE guild_id == {guild_id};")
        data = c.fetchall()
        num = 0
        for channel in data:
            data[num] = (channel[0], Val(channel[1]))
            num += 1
        return data

    def ignorechannel(guild_id, channel_id):
        t = (guild_id,)
        c.execute("SELECT channel_id FROM counter WHERE guild_id=?", t)
        counter_channel_id = c.fetchone()[0]
        if channel_id != counter_channel_id: return True
        return False

    def checkdouble(guild_id, user_id):
        t = (guild_id,)
        c.execute("SELECT user_id FROM counter WHERE guild_id=?", t)
        last_user_id = c.fetchone()[0]
        if user_id == last_user_id:
            t = (guild_id,)
            c.execute("UPDATE counter SET number=0, user_id=0 WHERE guild_id=?", t)
            conn.commit()
            return True
        return False

    def getnumber(guild_id):
        t = (guild_id,)
        c.execute("SELECT number FROM counter WHERE guild_id=?", t)
        return int(c.fetchone()[0])

    def getuser(guild_id):
        t = (guild_id,)
        c.execute("SELECT user_id FROM counter WHERE guild_id=?", t)
        return int(c.fetchone()[0])

    def gethighscore(guild_id):
        t = (guild_id,)
        c.execute("SELECT record FROM counter WHERE guild_id=?", t)
        return c.fetchone()[0]

    def gethighscores():
        c.execute("SELECT guild_id, record FROM counter ORDER BY record DESC LIMIT 5")
        return c.fetchall()

    def resetnumber(guild_id):
        t = (guild_id,)
        c.execute("UPDATE counter SET number=0, user_id=0 WHERE guild_id=?", t)
        conn.commit()

    def updatenumber(number, author_id, guild_id):
        t = (number, author_id, guild_id,)
        c.execute("UPDATE counter SET number=?, user_id=? WHERE guild_id=?", t)
        conn.commit()

    def highscore(number, guild_id):
        t = (guild_id,)
        c.execute("SELECT record FROM counter WHERE guild_id=?", t)
        record = c.fetchone()[0]
        if number > record:
            record = number
            t = (record, guild_id,)
            c.execute("UPDATE counter SET record=? WHERE guild_id=?", t)
            conn.commit()

    def setcountingchannel(channel_id, guild_id):
        t = (channel_id, guild_id,)
        c.execute("UPDATE counter SET channel_id=? WHERE guild_id=?", t)
        conn.commit()
