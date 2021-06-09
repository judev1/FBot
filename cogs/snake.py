from discord.ext import commands
from collections import deque
from random import randint, choice
from discord_components import Button, ButtonStyle, InteractionType
import asyncio

emojis = {
    "up": "⬆️",
    "down": "⬇️",
    "left": "⬅️",
    "right": "➡️"
}

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

    def won(self):
        if self.width * self.height == len(self.snake):
            return True
        return False

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

    @commands.command(name="snake", aliases=["snek"])
    async def _Snake(self, ctx):

        def embed():
            embed = self.bot.fn.embed(ctx.author, "Snake Game", game.board())
            embed.set_author(name=f"{game.score} points | {game.direction.upper()}")
            return embed

        def components(ignore):

            x = ["up", "down"]
            y = ["left", "right"]

            def button(direction):
                disabled = False
                if ignore in x and direction in x:
                    disabled = True
                elif ignore in y and direction in y:
                    disabled = True
                return Button(style=ButtonStyle.blue, emoji=emojis[direction], disabled=disabled)

            null = Button(style=ButtonStyle.grey, label="-", disabled=True)
            row_one = [null, button("up"), null]
            row_two = [button("left"), null, button("right")]
            row_three = [null, button("down"), null]

            return [row_one, row_two, row_three]

        user_id = ctx.author.id
        if user_id in self.games:
            ctx.send("You are already in a game!")
            return

        game = self.games[user_id] = snakegame()
        msg = await ctx.send(embed=embed(), components=components("right"))
        game.message_id = msg.id

        while game.alive:
            await asyncio.sleep(0.8)
            game.move()
            try: await msg.edit(embed=embed(), components=components(game.direction))
            except: break

        buttons = []
        if game.won():
            button = Button(style=ButtonStyle.green, label="You won!", disabled=True)
        else:
            button = Button(style=ButtonStyle.red, label="You died!", disabled=True)
        buttons.append(button)

        button = Button(style=ButtonStyle.green, label=f"Score: {game.score}", disabled=True)
        buttons.append(button)

        try: await msg.edit(embed=embed(), components=[buttons])
        except: pass

        del self.games[user_id]

    @commands.Cog.listener()
    async def on_button_click(self, res):
        user_id = res.author.id
        if user_id in self.games:
            if res.message.id == self.games[user_id].message_id:
                if hasattr(res.component, "emoji"):
                    emoji = res.component.emoji.name
                    for direction in emojis:
                        if emoji == emojis[direction]:
                            self.games[user_id].direction = direction
                            break
        await res.respond(type=InteractionType.DeferredUpdateMessage)

def setup(bot):
    bot.add_cog(snake(bot))