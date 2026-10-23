import enum

import discord
import httpx
import logging

from clients import helpr_client
from clients.helpr_client import HelprApiError
from src.bot.strings import FollowUps
from src.schemas import TicketUpdate
from src.utils.config import settings
from src.utils.crypto import create_hmac
from src.views.manage_message import TicketMessage

logger = logging.getLogger(__name__)

helpr_url = settings.HELPR_URL


class UpdateTicket:
    @staticmethod
    # TODO: Create buzz code enum rather than just string
    # TODO: Improve error handling
    async def _update(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
        *,
        endpoint: str,
    ):
        # let discord know this might take a while and not timeout
        await interaction.response.defer(ephemeral=True)

        try:
            updated_ticket = await helpr_client.post_ticket_action(
              endpoint, discord_id=str(interaction.user.id), ticket_id=ticket_details.ticket_id
            )
        except HelprApiError as err:
            if err.code is None:
              logger.error(str(err))
            await interaction.followup.send(str(err.code or FollowUps.GENERIC_ERROR), ephemeral=True)
            return


    @staticmethod
    async def claim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="claim"
        )

    @staticmethod
    async def unclaim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="unclaim"
        )

    @staticmethod
    async def resolve(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(
            ticket_details, interaction, endpoint="resolve"
        )
