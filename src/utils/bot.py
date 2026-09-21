import logging

import discord

intents = discord.Intents.default()
client = discord.Client(intents=intents)

logger = logging.getLogger(__name__)

@client.event
async def on_ready():
    logger.info(f"Successfully logged in as {client.user}!")
