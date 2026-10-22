import discord

from src.bot.strings import FollowUps
from src.utils.config import settings

async def generic_error_followup(interaction: discord.Interaction):
    await interaction.followup.send(
        content=FollowUps.GENERIC_ERROR,
        ephemeral=True,
    )
