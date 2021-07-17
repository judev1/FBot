from random import randint, choice
from discord.ext import commands
from collections import deque
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

        self.food_emojis = [":peach:", ":mango:", ":apple:", ":watermelon:", ":tangerine:",
                            ":banana:", ":pineapple:", ":pear:", ":blueberries:", ":eggplant:",
                            ":grapes:"]
        self.food = self.create_food_coords()

    def board(self):
        board = ":white_large_square:" * (self.width + 2) + "\n"
        for y in range(self.height):
            board += ":white_large_square:"
            for x in range(self.width):
                if (x, y) in self.snake:
                    if (x, y) == self.snake[0]:
                        if self.alive:
                            board += ":flushed:"
                        else:
                            board += ":skull:"
                    elif (x, y) == self.snake[-1]:
                        if self.alive:
                            board += ":yellow_circle:"
                        else:
                            board += ":white_circle:"
                    else:
                        if self.alive:
                            board += ":yellow_square:"
                        else:
                            board += ":white_large_square:"
                elif (x, y) == self.food:
                    if self.alive:
                        board += self.food_emoji
                    else:
                        board += ":radioactive:"
                else:
                    board += ":black_large_square:"
            board += ":white_large_square:\n"
        board += ":white_large_square:" * (self.width + 2)
        return board

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
        self.food_emoji = choice(self.food_emojis)
        x, y = randint(0, self.width-1), randint(0, self.height-1)
        while (x, y) in self.snake:
            x, y = randint(0, self.width-1), randint(0, self.height-1)
        return (x, y)

class snake(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @commands.command(name="snake", alliases=["snek"])
    async def _Snake(self, ctx):

        def speed():
            return 0.8

        def snake_embed():
            embed = self.bot.embed(ctx.author, "Snake Game", game.board())
            embed.set_author(name=f"{game.score} points | {game.direction.upper()}")
            return embed

        user_id = ctx.author.id
        if user_id in self.games:
            await ctx.reply("You are already in a game!")
            return

        game = self.games[user_id] = snakegame()
        msg = await ctx.send(embed=snake_embed())

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while game.alive:
            await asyncio.sleep(speed())
            game.move()
            try: await msg.edit(embed=snake_embed())
            except: break
        del self.games[user_id]

        await ctx.reply(f"**You died with a score of {game.score}!**")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id not in self.games: return
        emoji = reaction.emoji
        if emoji in emojis:
            self.games[user.id].direction = emojinames[emojis.index(emoji)]
        await reaction.message.remove_reaction(reaction, user)

def setup(bot):
    bot.add_cog(snake(bot))