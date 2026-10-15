import discord

from src.utils.config import settings

async def generic_error_followup(interaction: discord.Interaction):
    await interaction.followup.send(
        content="Something went wrong, ticket was not claimed\n"
        f"Please claim directly from [helpr]({settings.HELPR_URL})",
        ephemeral=True,
    )
