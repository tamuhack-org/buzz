
import discord
import logging

from src.services.ticket_service import TicketService
from src.clients.helpr_client import HelprApiError
from src.bot.strings import FollowUps
from src.schemas import TicketUpdate
from src.utils.config import settings

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
        if not interaction.message:
            logger.error(f"{endpoint} clicked but interaction.message was None")
            await interaction.response.send_message(
                FollowUps.GENERIC_ERROR, ephemeral=True
            )
            return

        # let discord know this might take a while and not timeout
        await interaction.response.defer(ephemeral=True)

        try:
            await TicketService().apply_action(
                endpoint,
                ticket_id=ticket_details.ticket_id,
                discord_id=str(interaction.user.id),
                message=interaction.message,
            )
        except HelprApiError as err:
            if err.code is None:
                logger.error(str(err))
            await interaction.followup.send(
                str(err.code or FollowUps.GENERIC_ERROR), ephemeral=True
            )
            return
        except Exception:
            logger.exception(f"{endpoint} failed")
            await interaction.followup.send(FollowUps.GENERIC_ERROR, ephemeral=True)

    @staticmethod
    async def claim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(ticket_details, interaction, endpoint="claim")

    @staticmethod
    async def unclaim(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(ticket_details, interaction, endpoint="unclaim")

    @staticmethod
    async def resolve(
        ticket_details: TicketUpdate,
        interaction: discord.Interaction,
    ):
        await UpdateTicket._update(ticket_details, interaction, endpoint="resolve")
