from .database import db
from time import time

db = db(verbose=False)

class Cooldowns:

    _commands = dict()
    _cooldowns = dict()

    def add_command(self, command, cooldowns):

        self._commands[command] = cooldowns
        setattr(self, command, dict())

    def cooldown(self, ctx):

        command = ctx.command.name
        user = ctx.author

        premium = int(db.premium(user))
        user = user.id

        command_cooldowns = self._commands[command]
        cooldowns = getattr(self, command)
        now = time()
        cooldown = 0

        if user in self._cooldowns:
            if now >= self._cooldowns[user]:
                del self._cooldowns[user]
            else:
                cooldown = self._cooldowns[user] - now

        if user in cooldowns:
            if now >= cooldowns[user]:
                del cooldowns[user]
            else:
                cooldown = cooldowns[user] - now

        if not cooldown:
            if premium:
                self._cooldowns[user] = now + 2
            else:
                self._cooldowns[user] = now + 8
            cooldowns[user] = now + command_cooldowns[premium]

        for user in self._cooldowns.copy():
            if now >= self._cooldowns[user]:
                del self._cooldowns[user]
            else: break

        for user in cooldowns.copy():
            if now >= cooldowns[user]:
                del cooldowns[user]
            else: break

        return cooldown

class Names:

    _names = dict()
    _expiries = dict()

    def get(self, obj_id):

        name = None
        if obj_id in self._names:
            name = self._names[obj_id]

        now = time()
        for obj_id in self._expiries.copy():
            if now >= self._expiries[obj_id]:
                del self._names[obj_id]
                del self._expiries[obj_id]

        return name

    def add(self, obj_id, name):

        now = time()
        self._names[obj_id] = name
        self._expiries[obj_id] = now + 10*60