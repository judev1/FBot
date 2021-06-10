from discord.ext import commands
import asyncio
from random import randint

emojis = ["⬆️", "⬇️"]
emojinames = ["forward-up", "forward-down"]

class dodgergame():

    def __init__(self):
        self.alive = True
        self.score = 0
        self.height = 5
        self.width = 8
        self.player = 4
        self.obstacles = list()
        self.obstacles_per_frame = 2
        self.frames_between_obstacles = 1
        self.frames_until_obstacle = 0
        self.direction = "forward"

    def board(self):
        msg = ""
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 and y == self.player:
                    if self.alive:
                        msg += ":rocket:"
                    else:
                        msg += ":boom:"
                elif [x, y] in self.obstacles:
                    msg += ":firecracker:"
                else:
                    msg += ":black_large_square:"
            msg += "\n"
        return msg

    def move(self):

        if self.direction == "forward-up":
            self.player -= 1
        elif self.direction == "forward-down":
            self.player += 1
        self.direction = "forward"

        if self.player < 0:
            self.player = 0
        elif self.player >= self.height:
            self.player = self.height - 1

        self.move_obstacles()
        self.check_collisions()

        self.frames_until_obstacle -= 1
        if self.frames_until_obstacle <= 0:
            self.frames_until_obstacle = self.frames_between_obstacles
            for i in range(self.obstacles_per_frame):
                self.create_obstacle()

    def check_collisions(self):
        for obstacle in self.obstacles:
            if obstacle[0] == 0:
                if obstacle[1] == self.player:
                    self.alive = False

    def move_obstacles(self):
        obstacles_to_remove = list()
        for index, obstacle in enumerate(self.obstacles):
            obstacle[0] -= 1
            if obstacle[0] < 0:
                obstacles_to_remove.append(index)
                self.score += 1

        self.obstacles = [obstacle for index, obstacle in
                          enumerate(self.obstacles) if not index in
                          obstacles_to_remove]

    def create_obstacle(self):
        obstacle = [self.width - 1, randint(0, self.height - 1)]
        self.obstacles.append(obstacle)

class dodger(commands.Cog):
    game = dodgergame()

    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="dodger")
    async def _Dodger(self, ctx):

        def dodger_embed():
            embed = self.bot.fn.embed(ctx.author, "Dodger Game", game.board())
            embed.set_author(name=f"{game.score} points | {game.direction.upper()}")
            return embed

        user_id = ctx.author.id
        if user_id in self.games:
            ctx.send("You are already in a game!")
            return

        game = self.games[user_id] = dodgergame()
        msg = await ctx.send(embed=dodger_embed())

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while game.alive:
            await asyncio.sleep(0.8)
            game.move()
            try: await msg.edit(embed=dodger_embed())
            except: break
        del self.games[user_id]

        await ctx.send(f"**You died with a score of {game.score}!**")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id not in self.games: return
        emoji = reaction.emoji
        if emoji in emojis:
            self.games[user.id].direction = emojinames[emojis.index(emoji)]
        await reaction.message.remove_reaction(reaction, user)

def setup(bot):
    bot.add_cog(dodger(bot))