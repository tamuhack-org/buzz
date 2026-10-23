import logging

import discord

from src.bot.client import client
from src.bot.strings import DMs
from src.exceptions.custom_exceptions import BadRequest, InternalServerError

logger = logging.getLogger(__name__)


class RoleService:
    async def give_role(self, *, role_id: int, user_id: int, server_id: int):
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
        except discord.NotFound:
            user = client.get_user(user_id) or await client.fetch_user(user_id)
            try:
                await user.send(DMs.NOT_IN_SERVER)
            except discord.Forbidden:
                # TODO: redirect to a helpr page with invite link and ask to rerun discord link
                logger.info("Could not DM user %s; their DMs may be closed", user_id)

            raise BadRequest(f"User {user_id} was not found in server {server_id}")

        if role not in member.roles:
            try:
                await member.add_roles(role)
            except discord.HTTPException as e:
                logger.exception(
                    f"Something went wrong when granting user {user_id} the role {role_id} in server {server_id}"
                )
                raise InternalServerError(
                    f"Failed to give user {user_id} the role {role_id} in server {server_id}\n {e}"
                )

        # successfully added role
        try:
            await member.send(DMs.WELCOME.format(mention=member.mention))
        except Exception:
            logger.exception("failed to DM welcome message to mentor")

        logger.info(f"user {user_id} now has the role {role_id} in server {server_id}")
