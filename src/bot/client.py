import logging
import discord

logger = logging.getLogger(__name__)

class BuzzClient(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        # NOTE: runs once on login
        await self.tree.sync()

    async def on_ready(self) -> None:
        # NOTE: runs on every connection (including reconnects)
        logger.info(f"Successfully logged in as {self.user}!")

client = BuzzClient()
