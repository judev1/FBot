from discord.ext import commands
from functions import predicate
from collections import deque
from random import randint
import asyncio

emojis = ["⬆️", "⬇️", "⬅️", "➡️"]
emojinames = ["up", "down", "left", "right"]

class snakegame():
    
    def __init__(self):
        self.alive = True
        self.score = 0
        self.width  = 8
        self.height = 8
        self.direction = "right"

        self.snake = deque()
        self.snake.appendleft((0, 4))
        self.snake.appendleft((1, 4))
        self.snake.appendleft((2, 4))

        self.food = self.create_food_coords()

    def board(self):
        output = f"**Score:** {self.score}\n"
        output += ":white_large_square:" * (self.width + 2) + "\n"
        for y in range(self.height):
            output += ":white_large_square:"
            for x in range(self.width):
                if (x, y) in self.snake:
                    if (x, y) == self.snake[0]:
                        if self.alive:
                            output += ":flushed:"
                        else:
                            output += ":skull:"
                    elif (x, y) == self.snake[-1]:
                        if self.alive:
                            output += ":yellow_circle:"
                        else:
                            output += ":white_circle:"
                    else:
                        if self.alive:
                            output += ":yellow_square:"
                        else:
                            output += ":white_large_square:"
                elif (x, y) == self.food:
                    if self.alive:
                        output += ":apple:"
                    else:
                        output += ":radioactive:"
                else:
                    output += ":black_large_square:"
            output += ":white_large_square:\n"
        output += ":white_large_square:" * (self.width + 2)
        return output

    def move(self):
        x, y = self.snake[0]
        direction = self.direction
        if direction == "up": y -= 1
        elif direction == "down": y += 1
        if direction == "left": x -= 1
        elif direction == "right": x += 1

        if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
            self.alive = False
            return
        
        if (x, y) in self.snake:
            self.alive = False
            return
        
        self.snake.appendleft((x, y))
        
        if (x, y) == self.food:
            self.food = self.create_food_coords()
            self.score += 1
        else:
            self.snake.pop()

    def create_food_coords(self):
        x, y = randint(0, self.width-1), randint(0, self.height-1)
        while (x, y) in self.snake:
            x, y = randint(0, self.width-1), randint(0, self.height-1)
        return (x, y)
    

class snake(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
        
    @commands.command(name="snake", alliases=["snek"])
    @commands.check(predicate)
    async def _Snake(self, ctx):

        user_id = ctx.author.id
        if user_id in self.games:
            ctx.send("You are already in a game!")
            return

        game = self.games[user_id] = snakegame()
        msg = await ctx.send(game.board())

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            await asyncio.sleep(0.8)
            game.move()
            await msg.edit(content=game.board())
            if not game.alive: break
        del self.games[user_id]

        fbux = game.score * 10
        self.bot.db.updatebal(ctx.author.id, fbux)
        await ctx.send("**You died, game over!**\n"
                       f"However you managed to earn **~~f~~ {fbux}**")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id not in self.games: return
        emoji = reaction.emoji
        if emoji in emojis:
            self.games[user.id].direction = emojinames[emojis.index(emoji)]        
        await reaction.message.remove_reaction(reaction, user)
        
def setup(bot):
    bot.add_cog(snake(bot))
