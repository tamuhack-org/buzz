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
    server_id = settings.SERVER_ID
    guild = client.get_guild(server_id)
    if guild is None:
        logger.error(
            f"Failed to find server {server_id}. Are you sure buzz is in this server?"
        )
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        return

    try:
        member = await guild.fetch_member(interaction.user.id)
    except discord.NotFound:
        await interaction.response.send_message(Checkout.NOT_USER, ephemeral=True)
        return

    role_id = settings.MENTOR_ROLE_ID
    role = guild.get_role(role_id)
    if role is None:
        logger.error(f"Could not find role {role_id} in server {server_id}")
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        return

    if role not in member.roles:
        await interaction.response.send_message(Checkout.NOT_MENTOR, ephemeral=True)
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        logger.exception("Failed to remove mentor role from user %s", member.id)
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        return

    await interaction.response.send_message(Checkout.SUCCESS, ephemeral=True)
    logger.info(f"Successfully checked out mentor {member.id}")
