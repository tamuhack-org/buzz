import logging

import discord
from discord import app_commands

from src.bot.strings import Checkout
from src.utils.config import settings

logger = logging.getLogger(__name__)


# NOTE: Workaround: Set high level permission to prevent everyone from seeing the command
# then override on discord client to allow mentors
@app_commands.command(name="checkout", description="removes mentor role")
@app_commands.default_permissions(administrator=True)
async def checkout(interaction: discord.Interaction):
    member = interaction.user
    if not isinstance(member, discord.Member):
        await interaction.response.send_message(Checkout.NOT_USER, ephemeral=True)
        return

    role_id = settings.MENTOR_ROLE_ID
    role = interaction.guild.get_role(role_id) if interaction.guild else None
    if role is None:
        logger.error(f"Role {role_id} was not found in server {interaction.guild_id}")
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        return

    if role not in member.roles:
        await interaction.response.send_message(Checkout.NOT_MENTOR, ephemeral=True)
        return

    try:
        await member.remove_roles(role)
    except discord.HTTPException:
        logger.exception(f"Failed to remove role {role_id} from user {member.id}")
        await interaction.response.send_message(Checkout.ERROR, ephemeral=True)
        return

    await interaction.response.send_message(Checkout.SUCCESS, ephemeral=True)
    logger.info(f"Successfully checked out mentor {member.id}")
