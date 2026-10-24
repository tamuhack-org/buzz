import logging

import discord
from discord import app_commands

from src.bot.client import client
from src.bot.strings import Checkout
from src.utils.config import settings

logger = logging.getLogger(__name__)


# NOTE: Workaround: Set high level permission to prevent everyone from seeing the command
# then override on discord client to allow mentors
@app_commands.command(name="checkout", description="removes mentor role")
@app_commands.default_permissions(administrator=True)
async def checkout(interaction: discord.Interaction):
    try:
        await interaction.response.send_message(Checkout.CHECKING_OUT, ephemeral=True)
    except discord.NotFound:
        logger.warning(
            f"checkout from {interaction.user.id} expired before it could be acknowledged"
        )
        return

    server_id = settings.SERVER_ID
    guild = client.get_guild(server_id)
    if guild is None:
        logger.error(
            f"Failed to find server {server_id}. Are you sure buzz is in this server?"
        )
        await interaction.edit_original_response(content=Checkout.ERROR)
        return

    try:
        member = await guild.fetch_member(interaction.user.id)
    except discord.NotFound:
        await interaction.edit_original_response(content=Checkout.NOT_USER)
        return

    role_id = settings.MENTOR_ROLE_ID
    role = guild.get_role(role_id)
    if role is None:
        logger.error(f"Could not find role {role_id} in server {server_id}")
        await interaction.edit_original_response(content=Checkout.ERROR)
        return

    if role not in member.roles:
        await interaction.edit_original_response(content=Checkout.NOT_MENTOR)
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        logger.exception("Failed to remove mentor role from user %s", member.id)
        await interaction.edit_original_response(content=Checkout.ERROR)
        return

    logger.info(f"Successfully checked out mentor {member.id}")

    try:
        await member.send(Checkout.SUCCESS)
    except discord.HTTPException:
        # DMs closed
        logger.info("Could not DM checkout confirmation to %s", member.id)
        #doesn't really matter since they lose access to channel lol
        await interaction.edit_original_response(content=Checkout.SUCCESS)
        return

    try:
        await interaction.delete_original_response()
    except discord.HTTPException:
        pass
