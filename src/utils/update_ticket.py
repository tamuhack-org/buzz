import enum

import discord
import httpx
import logging

from src.bot.strings import FollowUps
from src.schemas import TicketUpdate
from src.utils.config import settings
from src.utils.crypto import create_hmac
from src.views.manage_message import TicketMessage

logger = logging.getLogger(__name__)

helpr_url = settings.HELPR_URL


class HelprError(enum.StrEnum):
    DISCORD_NOT_LINKED = FollowUps.DISCORD_NOT_LINKED
    HAS_EXISTING_TICKET = FollowUps.HAS_EXISTING_TICKET
    TICKET_ALREADY_CLAIMED = FollowUps.TICKET_ALREADY_CLAIMED
    TICKET_MISMATCH = FollowUps.TICKET_MISMATCH


class UpdateTicket:
    @staticmethod
    # TODO: Create buzz code enum rather than just string
    # TODO: Improve error handling
    async def _update(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
        *,
        endpoint: str,
        errors: type[HelprError],
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
        try:
            error = HelprError[code]
        except:
            error = None

        if error in errors:
            await interaction.followup.send(
                content=str(error),
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

        # no need to update state directly since helper forces refresh on buzz when state changes
        # TODO: but theres a small delay so ponder if this should remain
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
            ticket_details, interaction, endpoint="claim", errors=HelprError
        )

    @staticmethod
    async def unclaim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="unclaim", errors=HelprError
        )

    @staticmethod
    async def resolve(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="resolve", errors=HelprError
        )
