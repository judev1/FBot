from discord.ext import commands
import asyncio
from collections import deque
from random import randint

emojis = ["⬆️", "⬇️", "⬅️", "➡️"]
emojinames = ["up", "down", "left", "right"]

class snakegame():
    
    def __init__(self):
        self.alive = True
        self.score = 0
        self.width  = 8
        self.height = 8

        self.snake = deque()
        self.snake.appendleft((0, 4))
        self.snake.appendleft((1, 4))
        self.snake.appendleft((2, 4))

        self.food = self.create_food_coords()

    def board(self):
        output = f"**Score:** {self.score}\n"
        for y in range(self.height):
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
            output += "\n"
        return output

    def move(self, direction):
        x, y = self.snake[0]
        if direction == "up": y -= 1
        if direction == "down": y += 1
        if direction == "left": x -= 1
        if direction == "right": x += 1

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
        
    @commands.command(name="snake")
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    async def _Snake(self, ctx):

        game = snakegame()
        msg = await ctx.send(game.board())

        for emoji in emojis:
            await msg.add_reaction(emoji)

        def check(reaction, user):
            emoji = (str(reaction.emoji) in emojis)
            author = (user == ctx.author)
            message = (reaction.message.id == msg.id)
            return emoji and author and message


        wait = self.bot.wait_for
        async def forreaction():
            #timeout =  max(2 - (3 * game.score / 40), 0.5)
            timeout = 0.8
            return await wait("reaction_add", timeout=timeout, check=check)

        lastmove = "right"
        while True:
            try:
                reaction, user = await forreaction()
                await msg.remove_reaction(reaction, user)
            except asyncio.exceptions.TimeoutError:
                reaction = None
            except:
                return
            if reaction:
                lastmove = emojinames[emojis.index(reaction.emoji)]
                game.move(lastmove)
            else: game.move(lastmove)
            
            await msg.edit(content=game.board())
            if not game.alive: break

        fbux = game.score * 10
        self.bot.db.updatebal(ctx.author.id, fbux)
        await ctx.send("**You died, game over!**\n"
                       f"However you managed to earn **~~f~~ {fbux}**")

    @_Snake.error
    async def on_command_error(self, ctx, error):
        if type(error) is commands.CommandOnCooldown:
            wait = round(error.retry_after)
            await ctx.send(f"You must wait another {wait} seconds before playing snake again")
        
def setup(bot):
    bot.add_cog(snake(bot))
