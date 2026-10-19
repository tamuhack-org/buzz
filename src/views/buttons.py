from enum import Enum
import logging

import discord

from src.schemas import TicketDetails, TicketUpdate
from src.utils.config import settings
from src.utils.followups import generic_error_followup

logger = logging.getLogger(__name__)


class TicketState(str, Enum):
    AVAILABLE = "available"
    CLAIMED = "claimed"
    RESOLVED = "resolved"
    ERROR = "error"


# NOTE: Looks like discord doesn't allow you to disable buttons only for some users :(

# TODO: Fix literally everything to do with buttons
class TicketButtons(discord.ui.View):
    async def _make_ticket_update(
        self, interaction: discord.Interaction
    ) -> TicketUpdate | None:
        message = interaction.message
        if message is None:
            await generic_error_followup(interaction)
            return None

        ticket_data = self.ticket_details.model_dump()
        ticket_data.update(
            channel_id=str(message.channel.id),
            message_id=str(message.id),
        )

        return TicketUpdate.model_validate(ticket_data)

    def __init__(
        self, ticket_details: TicketDetails, state: TicketState = TicketState.AVAILABLE
    ):
        timeout = 172800  # timeout in 2 days
        super().__init__(timeout=timeout)
        self.ticket_details = ticket_details

        if state == TicketState.AVAILABLE:
            button = discord.ui.Button(
                label="Claim Ticket", style=discord.ButtonStyle.blurple
            )
            button.callback = self.claim
            self.add_item(button)

        elif state == TicketState.CLAIMED:
            resolve_button = discord.ui.Button(
                label="Resolve Ticket", style=discord.ButtonStyle.green
            )
            resolve_button.callback = self.resolve
            self.add_item(resolve_button)

            # TODO: if ticket is unclaimed, look into renotifying?
            unclaim_button = discord.ui.Button(
                label="Unclaim Ticket", style=discord.ButtonStyle.danger
            )
            unclaim_button.callback = self.unclaim
            self.add_item(unclaim_button)

        else:
            # don't want view ticket if resolved
            return

        self.add_item(
            discord.ui.Button(
                label="View Ticket",
                url=f"{settings.HELPR_URL}/mentor",
            )
        )

    # TODO: look into reducing duplicate code here
    async def claim(self, interaction: discord.Interaction):
        from src.views.update_ticket import UpdateTicket

        ticket_update = await self._make_ticket_update(interaction)
        if ticket_update is None:
            await generic_error_followup(interaction)
            return

        await UpdateTicket.claim(ticket_update, interaction)

    async def resolve(self, interaction: discord.Interaction):
        from src.views.update_ticket import UpdateTicket

        ticket_update = await self._make_ticket_update(interaction)
        if ticket_update is None:
            await generic_error_followup(interaction)
            return

        await UpdateTicket.resolve(ticket_update, interaction)

    async def unclaim(self, interaction: discord.Interaction):
        from src.views.update_ticket import UpdateTicket

        ticket_update = await self._make_ticket_update(interaction)
        if ticket_update is None:
            await generic_error_followup(interaction)
            return

        await UpdateTicket.unclaim(ticket_update, interaction)
