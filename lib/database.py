from datetime import datetime
import aiomysql
import time
import asyncio

def connect(settings):
    coro = _create_pool(settings)
    return aiomysql.pool._PoolContextManager(coro)

async def _create_pool(settings):
    pool = Pool(settings)
    async with pool._cond:
        await pool._fill_free_pool(False)
    # await ((await pool.connection()).rollback()).close()
    return pool

class Connection:

    def __init__(self, pool, connection, autoclose=True):
        self.pool = pool
        self.connection = connection
        self.autoclose = autoclose

    async def execute(self, query, *args):
        if not hasattr(self, "cursor"):
            self.cursor = await self.connection.cursor()
        await self.cursor.execute(query, *args)

    async def fetchone(self):
        result = await self.cursor.fetchone()
        if self.autoclose: await self.close()
        return result

    async def fetchall(self):
        result = await self.cursor.fetchall()
        if self.autoclose: await self.close()
        return result

    async def close(self):
        await self.cursor.close()
        self.pool.release(self.connection)

class Pool(aiomysql.Pool):

    def __init__(self, settings):
        super().__init__(
            host=settings.database.host,
            user=settings.database.user,
            password=settings.database.password,
            db=settings.database.database,
            minsize=1,
            maxsize=100,
            echo=False,
            pool_recycle=-1,
            loop=asyncio.get_event_loop(),
            autocommit=True
        )

    async def connection(self, autoclose=True):
        return Connection(self, await self.acquire(), autoclose)

    # General

    async def addguild(self, guild_id):
        c = await self.connection()
        t = (guild_id, time.time())
        await c.execute("""INSERT INTO guilds (
                            guild_id, notice,
                            prefix, modtoggle, priority, mode, language,
                            name, picture, triggers
                        )
                        VALUES (
                            %s, %s,
                            'fbot', 'off', 'all', 'default', 'english',
                            '', '', '{}'
                        );""", t)
        await c.close()
        await self.addcounting(guild_id)

    async def addcounting(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("""INSERT INTO counting (
                            guild_id, channel_id, number, user_id, record
                        )
                        VALUES (
                            %s, 0, 0, 0, 0
                        );""", t)
        await c.close()

    async def removeguild(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("DELETE FROM guilds WHERE guild_id=%s;", t)
        await c.execute("DELETE FROM channels WHERE guild_id=%s;", t)
        await c.execute("DELETE FROM counting WHERE guild_id=%s;", t)
        await c.close()

    async def addchannel(self, channel_id, guild_id):
        c = await self.connection(autoclose=False)
        t = (channel_id,)
        await c.execute("SELECT * FROM channels where channel_id=%s;", t)
        if not await c.fetchone():
            t = (guild_id, channel_id)
            await c.execute("""INSERT INTO channels (
                            guild_id, channel_id, status,
                            shout
                        )
                        VALUES (
                            %s, %s, 'off',
                            'no'
                        );""", t)
        await c.close()

    # Config

    async def changemodtoggle(self, guild_id, modtoggle):
        c = await self.connection()
        t = (modtoggle, guild_id)
        await c.execute("UPDATE guilds SET modtoggle=%s WHERE guild_id=%s;", t)
        await c.close()

    async def getmodtoggle(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT modtoggle FROM guilds WHERE guild_id=%s;", t)
        return (await c.fetchone())[0]

    async def changemode(self, guild_id, mode):
        c = await self.connection()
        t = (mode, guild_id)
        await c.execute("UPDATE guilds SET mode=%s WHERE guild_id=%s;", t)
        await c.close()

    async def getmode(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT mode FROM guilds WHERE guild_id=%s;", t)
        return (await c.fetchone())[0]

    async def getlang(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT language FROM guilds WHERE guild_id=%s;", t)
        return (await c.fetchone())[0]

    async def changestatus(self, channel_id, status):
        c = await self.connection()
        t = (status, channel_id)
        await c.execute("UPDATE channels SET status=%s WHERE channel_id=%s;", t)
        await c.close()

    async def getstatus(self, channel_id):
        c = await self.connection()
        t = (channel_id,)
        await c.execute("SELECT status FROM channels WHERE channel_id=%s;", t)
        status = await c.fetchone()
        if not status:
            return None
        return status[0]

    async def getallstatus(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT channel_id, status FROM channels WHERE guild_id=%s;", t)
        newdata = []
        for channel in await c.fetchall():
            newdata.append(channel)
        return newdata

    # Notices

    async def addnotice(self, date, title, message):
        c = await self.connection()
        t = (date, title, message)
        await c.execute("""INSERT INTO notices (
                        date, title, message
                    )
                    VALUES (
                        %s, %s, %s
                    );""", t)
        await c.close()

    async def editnotice(self, title, message):
        c = await self.connection()
        t = (title, message, self.getlastnotice()[0])
        await c.execute(f"UPDATE notices SET title=%s, message=%s WHERE date=%s;", t)
        return await c.fetchone()

    async def getlastnotice(self):
        c = await self.connection()
        await c.execute(f"SELECT * FROM notices ORDER BY date DESC LIMIT 1;")
        return await c.fetchone()

    async def getservernotice(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute(f"SELECT notice FROM guilds WHERE guild_id=%s;", t)
        return (await c.fetchone())[0]

    async def updateservernotice(self, guild_id):
        c = await self.connection()
        t = (time.time(), guild_id)
        await c.execute(f"UPDATE guilds SET notice=%s WHERE guild_id=%s;", t)
        await c.close()

    # Users

    async def register(self, user_id):
        c = await self.connection(autoclose=False)
        t = (user_id,)
        await c.execute("SELECT user_id FROM users WHERE user_id=%s;", t)
        if await c.fetchone() is None:
            await c.execute(f"""INSERT INTO users (
                            user_id, ppsize,
                            commands, triggers,
                            title, colour, emoji, say, delete_say, claims
                        )
                        VALUES (
                            %s, -1,
                            0, 0,
                            '', {0xf42f42}, '', 'fbot', 'yes', 0
                        );""", t)
        await c.close()

    async def gettop(self, toptype, amount, obj_id):

        if toptype == "votes":
            TABLE, DATA, ID = "votes", "total_topvotes, total_bfdvotes, total_dblvotes", "user_id"
        elif toptype == "counting":
            TABLE, DATA, ID = "counting", "record", "guild_id"
        if toptype == "votes":
            ORDER = "total_topvotes + total_bfdvotes + total_dblvotes"
        else:
            ORDER = DATA

        c = await self.connection(autoclose=False)
        await c.execute(f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC LIMIT {amount};")
        top = await c.fetchall()

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
            await c.execute(f"SELECT {ID}, {DATA} FROM {TABLE} ORDER BY {ORDER} DESC;")
            for rank, data in enumerate(await c.fetchall()):
                if data[0] == obj_id:
                    score = sum(data[1:])
                    break

        await c.close()
        return (top, score, rank + 1)

    # Voting

    async def addvoter(self, user_id):
        c = await self.connection(autoclose=False)
        t = (user_id,)
        await c.execute("SELECT user_id FROM votes WHERE user_id=%s;", t)
        if not await c.fetchone():
            await c.execute("""INSERT INTO votes (
                            user_id,
                            topvotes, dblvotes, bfdvotes,
                            total_topvotes, total_dblvotes, total_bfdvotes,
                                last_topvote, last_dblvote, last_bfdvote
                        )
                        VALUES (
                            %s,
                            0, 0, 0,
                            0, 0, 0,
                            0, 0, 0
                        );""", t)
        await c.close()

    async def vote(self, user_id, site):
        user_id = int(user_id)
        self.addvoter(user_id)

        c = await self.connection()
        t = (user_id,)
        await c.execute(f"UPDATE votes SET {site}votes={site}votes+1, "
                    f"total_{site}votes=total_{site}votes+1, "
                    f"last_{site}vote={time.time()} WHERE user_id=%s;", t)

        await c.close()

    async def nextvote(self, user_id, site):
        c = await self.connection()
        user_id = int(user_id)
        t = (user_id,)
        await c.execute(f"SELECT last_{site}vote FROM votes where user_id=%s;", t)
        lastvote = await c.fetchone()
        if not lastvote:
            return None
        lastvote = lastvote[0]
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
        if hours == 0 or mins == 0:
            return None
        return (mins, hours)

    # Prefix

    async def changeprefix(self, guild_id, prefix):
        c = await self.connection()
        t = (prefix, guild_id)
        await c.execute("UPDATE guilds SET prefix=%s WHERE guild_id=%s;", t)
        await c.close()

    async def getprefix(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT prefix FROM guilds WHERE guild_id=%s;", t)
        return (await c.fetchone())[0]

    async def changepriority(self, guild_id, priority):
        c = await self.connection()
        t = (priority, guild_id)
        await c.execute("UPDATE guilds SET priority=%s WHERE guild_id=%s;", t)
        await c.close()

    async def getpriority(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT priority FROM guilds WHERE guild_id=%s;", t)
        try:
            return (await c.fetchone())[0]
        except:
            print("EERORROROR getprefix", guild_id)

    # ppsize

    async def getppsize(self, user_id):
        c = await self.connection()
        t = (user_id,)
        await c.execute("SELECT ppsize FROM users WHERE user_id=%s;", t)
        return (await c.fetchone())[0]

    async def updateppsize(self, user_id, size):
        c = await self.connection()
        t = (size, user_id)
        await c.execute("UPDATE users SET ppsize=%s WHERE user_id=%s;", t)
        await c.close()

    # Stats

    async def usecommand(self, user_id):
        c = await self.connection()
        t = (user_id,)
        await c.execute("UPDATE users SET commands=commands+1 WHERE user_id=%s;", t)
        await c.close()

    async def usetrigger(self, user_id):
        c = await self.connection()
        t = (user_id,)
        await c.execute("UPDATE users SET triggers=triggers+1 WHERE user_id=%s;", t)
        await c.close()

    # Counting

    async def checkdouble(self, guild_id, user_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT user_id FROM counting WHERE guild_id=%s;", t)
        if user_id == (await c.fetchone())[0]:
            c = await self.connection()
            t = (guild_id,)
            await c.execute("UPDATE counting SET number=0, user_id=0 WHERE guild_id=%s;", t)
            await c.close()
            return True
        return False

    async def getnumber(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT number FROM counting WHERE guild_id=%s;", t)
        return int((await c.fetchone())[0])

    async def getuser(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT user_id FROM counting WHERE guild_id=%s;", t)
        return int((await c.fetchone())[0])

    async def resetnumber(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("UPDATE counting SET number=0, user_id=0 WHERE guild_id=%s;", t)
        await c.close()

    async def updatenumber(self, number, author_id, guild_id):
        c = await self.connection()
        t = (number, author_id, guild_id,)
        await c.execute("UPDATE counting SET number=%s, user_id=%s WHERE guild_id=%s;", t)

        t = (guild_id,)
        await c.execute("SELECT record FROM counting WHERE guild_id=%s;", t)
        if number > (await c.fetchone())[0]:
            t = (number, guild_id,)
            await c.execute("UPDATE counting SET record=%s WHERE guild_id=%s;", t)
            await c.close()

    async def gethighscore(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT record FROM counting WHERE guild_id=%s;", t)
        return (await c.fetchone())[0]

    async def gethighscores(self):
        c = await self.connection()
        await c.execute("SELECT guild_id, record FROM counting ORDER BY record DESC LIMIT 5;")
        return await c.fetchall()

    async def setcountingchannel(self, channel_id, guild_id):
        c = await self.connection()
        t = (channel_id, guild_id)
        await c.execute("UPDATE counting SET channel_id=%s WHERE guild_id=%s;", t)
        await c.close()

    async def removecountingchannel(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("UPDATE counting SET channel_id=0 WHERE guild_id=%s;", t)
        await c.close()

    async def getcountingchannel(self, guild_id):
        c = await self.connection()
        t = (guild_id,)
        await c.execute("SELECT channel_id FROM counting WHERE guild_id=%s;", t)
        channel_id = await c.fetchone()
        if not channel_id:
            return 0
        return channel_id[0]