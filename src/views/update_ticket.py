import discord
import httpx
import logging

from src.schemas import TicketUpdate
from src.utils.config import settings
from src.utils.crypto import create_hmac
from src.views.ticket_message import TicketMessage

logger = logging.getLogger(__name__)


class UpdateTicket:
    @staticmethod
    async def claim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        userId = str(interaction.user.id)
        ticketId = ticket_details.ticket_id
        logger.info(f"Attemping to claim ticket: {ticketId} for user: {userId}")

        await interaction.response.defer(
            ephemeral=True
        )  # let discord know this might take a while and not timeout

        url = f"{settings.HELPR_URL}/api/tickets/claim"
        payload = {"discordId": userId, "ticketId": ticketId}
        headers = create_hmac(payload)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            data = response.json()
            logger.info(f"Claim ticket post request result: {response.status_code}")

            if data.get("code") == "DISCORD_NOT_LINKED":
                # discord account not linked
                link_url = f"{settings.HELPR_URL}/link/discord"
                # send private followup with url to link account
                await interaction.followup.send(
                    content=f"Your helpr account isn't linked to your discord! [Click here to link your Discord]({link_url})",
                    ephemeral=True,
                )
                return

            elif data.get("code") == "HAS_EXISTING_TICKET":
                link_url = f"{settings.HELPR_URL}/mentor"
                await interaction.followup.send(
                    content="You already have an active ticket. Before claiming another, either mark it as finished or unclaim it.\n"
                    f"[Manage your ticket here]({link_url})",
                    ephemeral=True,
                )
                return

            elif data.get("code") == "TICKET_ALREADY_CLAIMED":
                await interaction.followup.send(
                    content="This ticket has already been claimed",
                    ephemeral=True,
                )
                return

            elif response.status_code != 200:
                logger.info(f"Claim ticket failed: {response.text}")
                await interaction.followup.send(
                    content="Something went wrong, ticket was not claimed",
                    ephemeral=True,
                )
                return

            updated_ticket = TicketUpdate.model_validate(data.get("ticket"))

            await TicketMessage.update_ticket_message(updated_ticket)
