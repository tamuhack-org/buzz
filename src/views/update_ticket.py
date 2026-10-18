import enum

import discord
import httpx
import logging

from src.schemas import TicketUpdate
from src.utils.config import settings
from src.utils.crypto import create_hmac
from src.views.ticket_message import TicketMessage

logger = logging.getLogger(__name__)

helpr_url = settings.HELPR_URL
errors = {
    "DISCORD_NOT_LINKED": f"Your helpr account isn't linked to your discord! [Click here to link your Discord]({helpr_url}/link/discord)",
    "HAS_EXISTING_TICKET": f"You already have an active ticket. Before claiming another, either mark it as finished or unclaim it.\n[Manage your ticket here]({helpr_url})",
    "TICKET_ALREADY_CLAIMED": "This ticket has already been claimed",
    "TICKET_MISMATCH": f"You have no claimed ticket or your claimed ticket differs from the ticket you're trying to unclaim. No changes were made.\n[Manage your ticket here]({helpr_url})",
}

class UpdateTicket:
    @staticmethod
    # TODO: Create buzz code enum rather than just string
    # TODO: Improve error handling
    async def _update(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
        *,
        endpoint: str,
        errors: dict[str, str],
    ):
        # let discord know this might take a while and not timeout
        # TODO: Look into if this is really necessary?
        await interaction.response.defer(ephemeral=True)

        payload = {
            "discordId": str(interaction.user.id),
            "ticketId": ticket_details.ticket_id,
        }
        headers = create_hmac(payload)
        url = f"{settings.HELPR_URL}/api/tickets/{endpoint}"

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)

        data = response.json()
        code = data.get("code")

        if code in errors:
            await interaction.followup.send(
                content=errors[code],
                ephemeral=True,
            )
            return

        if response.status_code != 200:
            helpr_url = settings.HELPR_URL
            logger.error(f"{endpoint} failed: {response.text}")
            await interaction.followup.send(
                content=f"Something went wrong.\nPlease manage ticket directly from [helpr]({helpr_url})",
                ephemeral=True,
            )
            return

        try:
            updated_ticket = TicketUpdate.model_validate(data.get("ticket"))
            await TicketMessage.update_ticket_message(updated_ticket, interaction)
        except Exception as err:
            helpr_url = settings.HELPR_URL
            logger.error(f"Failed to update existing message: {err}")
            await interaction.followup.send(
                content=f"Something went wrong.\nPlease manage ticket directly from [helpr]({helpr_url})",
                ephemeral=True,
            )

    @staticmethod
    async def claim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="claim", errors=errors
        )

    @staticmethod
    async def unclaim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="unclaim", errors=errors
        )

    @staticmethod
    async def resolve(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="resolve", errors=errors
        )

