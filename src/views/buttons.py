import logging

import discord
import httpx

from src.schemas import TicketDetails, TicketUpdate
from src.utils.config import settings
from src.utils.crypto import create_hmac
from src.utils.followups import generic_error_followup

logger = logging.getLogger(__name__)


#TODO: Fix literally everything to do with buttons
class TicketButtons(discord.ui.View):
    def __init__(self, ticket_details: TicketDetails):
        timeout = 172800  # timeout in 2 days
        super().__init__(timeout=timeout)
        self.ticket_details = ticket_details

        self.add_item(
            discord.ui.Button(
                label="View Ticket",
                url=f"{settings.HELPR_URL}/mentor",
            )
        )

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        from src.views.update_ticket import UpdateTicket

        # TODO: add button to unclaim/resolve (only for claimed user)
        if interaction.message is None:
            await generic_error_followup(interaction)
            return
        
        ticket_update = TicketUpdate(
            **self.ticket_details.model_dump(),
            channel_id = str(interaction.message.channel.id),
            message_id= str(interaction.message.id)
        )

        await UpdateTicket.claim(ticket_update, interaction, button)
