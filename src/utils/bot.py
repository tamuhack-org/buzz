import logging

import discord

from src.exceptions.custom_exceptions import BadRequest

intents = discord.Intents.default()
client = discord.Client(intents=intents)

logger = logging.getLogger(__name__)


@client.event
async def on_ready():
    logger.info(f"Successfully logged in as {client.user}!")


# TODO: tie this file together better
class BotStuff:
    @staticmethod
    async def give_role(*, role_id: int, user_id: int, server_id: int):
        logger.info(
            f"attempting to give user {user_id} the role {role_id} in server {server_id}"
        )
        guild = client.get_guild(server_id)
        if guild is None:
            raise BadRequest(f"Bot is not connected to server {server_id}")

        role = guild.get_role(role_id)
        if role is None:
            raise BadRequest(f"Role {role_id} was not found in server {server_id}")

        try:
            member = await guild.fetch_member(user_id)
        except discord.NotFound as e:
            raise BadRequest(f"User {user_id} was not found in server {server_id}")

        if role not in member.roles:
            try:
                await member.add_roles(role)
            except Exception as e:
                logger.exception(
                    f"Something went wrong when grating user {user_id} the role {role_id} in server {server_id}\n {e}"
                )

        logger.info(f"user {user_id} now has the role {role_id} in server {server_id}")
