from time import time

class Cooldowns:

    _commands = dict()
    _cooldowns = dict()

    def __init__(self, devs, premium):
        self._devs = devs
        self._premium = premium

    def add(self, command, cooldowns):

        self._commands[command] = cooldowns
        setattr(self, command, dict())

    def get(self, user, command):

        if user in self._devs:
            return 0

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
            premium = int(user in self._premium)
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

class Cache:

    def __init__(self, devs, premium):

        self.cooldowns = Cooldowns(devs, premium)
        self.names = Names()