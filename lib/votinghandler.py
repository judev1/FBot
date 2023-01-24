from discord import Client
from aiohttp import web
import asyncio
import logging

logging.getLogger("aiohttp.server").setLevel(logging.CRITICAL)

class VotingHandler:

    def __init__(self, bot: Client):

        async def start():
            app = web.Application(loop=self.bot.loop)
            app.router.add_post("/bfdvote", self.on_bfd_post)
            app.router.add_post("/dblvote", self.on_dbl_post)

            runner = web.AppRunner(app)
            await runner.setup()

            port = self.bot.settings.voting_port
            server = web.TCPSite(runner, "0.0.0.0", port)
            await server.start()

        self.bot = bot

        loop = asyncio.get_event_loop()
        loop.run_until_complete(start())

    async def on_bfd_post(self, request):
        auth = request.headers.get("Authorization")
        if self.bot.settings.tokens.auth != auth:
            return web.Response(status=401)

        data = await request.json()
        self.bot.dispatch("vote", "discords", data)
        return web.Response(status=200)

    async def on_dbl_post(self, request):
        auth = request.headers.get("Authorization")
        if self.bot.settings.tokens.auth != auth:
            return web.Response(status=401)

        data = await request.json()
        self.bot.dispatch("vote", "discordbotlist", data)
        return web.Response(status=200)