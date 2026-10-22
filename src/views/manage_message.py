import discord
import logging
from fastapi import HTTPException

from src.bot.strings import DMs
from src.schemas import TicketDetails, TicketUpdate, TicketState
from src.utils.bot import client
from src.utils.config import settings

from src.exceptions.custom_exceptions import (
    InvalidChannelType,
    MessageNotFound,
    ChannelNotFound,
)

from src.views.embeds import TicketEmbeds
from src.views.messages import TicketMessages
from src.views.buttons import TicketButtons

logger = logging.getLogger(__name__)


# TODO: look into what should remain in views and what should go in a templates fodler
class TicketMessage:
    @staticmethod
    async def get_ticket_message(ticket: TicketUpdate) -> discord.Message:
        channel_id = int(ticket.channel_id)
        message_id = int(ticket.message_id)
        # looks up local cache
        channel = client.get_channel(channel_id)
        if channel is None:
            # http request
            channel = await client.fetch_channel(channel_id)

        if channel is None or not isinstance(channel, discord.TextChannel):
            raise InvalidChannelType("text channel", ticket.channel_id)

        message = await channel.fetch_message(message_id)
        if not message:
            raise MessageNotFound(ticket.message_id, ticket.channel_id)

        return message

    @staticmethod
    async def create_ticket_message(ticket_details: TicketDetails):
        logger.info("Attemping to ping mentors")
        channel = client.get_channel(settings.MENTOR_CHANNEL_ID)
        if not channel:
            logger.info("Provided mentor channel ID not found")
            raise ChannelNotFound(str(settings.MENTOR_CHANNEL_ID))

        if not isinstance(channel, (discord.TextChannel)):
            logger.info("Provided mentor channel is not a text channel")
            raise InvalidChannelType("text channel", str(settings.MENTOR_CHANNEL_ID))

        content = TicketMessages.ticket_available(ticket_details)
        embed = TicketEmbeds.ticket_available(ticket_details)
        view = TicketButtons(ticket_details)

        message = await channel.send(content=content, embed=embed, view=view)
        message_info = {
            "channel_id": str(message.channel.id),
            "message_id": str(message.id),
        }

        logger.info("Mentors pinged!")

        return {
            "status_code": 200,
            "message": "Message sent to mentors!",
            "message_info": message_info,
        }

    @staticmethod
    async def update_ticket_message(
        ticket_details: TicketUpdate, interaction: discord.Interaction | None = None
    ):
        # TODO: look into interaction.edit_original_response webhook dying
        if interaction is not None:
            message_editor = interaction.edit_original_response
        else:
            message = await TicketMessage.get_ticket_message(ticket_details)
            message_editor = message.edit

        if ticket_details.resolved and ticket_details.claimant is not None:
            state = TicketState.RESOLVED
            content = TicketMessages.ticket_resolved(ticket_details)
            embed = TicketEmbeds.ticket_resolved(ticket_details)

        elif ticket_details.claimant and ticket_details.claimant.user_id is not None:
            state = TicketState.CLAIMED
            content = TicketMessages.ticket_claimed(ticket_details)
            embed = TicketEmbeds.ticket_claimed(ticket_details)

        elif not ticket_details.claimant:
            state = TicketState.AVAILABLE
            content = TicketMessages.ticket_available(ticket_details)
            embed = TicketEmbeds.ticket_available(ticket_details)

        else:
            # some kinda indeterminant error state
            state = TicketState.ERROR
            content = TicketMessages.ticket_available(ticket_details)
            embed = TicketEmbeds.ticket_available(ticket_details)
            view = TicketButtons(ticket_details, state)
            await message_editor(content=content, embed=embed, view=view)
            raise HTTPException(status_code=422, detail="ticket state inconsistent")

        view = TicketButtons(ticket_details, state)
        await message_editor(
            content=content,
            embed=embed,
            view=view,
        )

    # TODO: maybe move to a dedicated dm method?
    @staticmethod
    async def _notify_claimant(ticket_details: TicketUpdate):
        claimant_id = (
            ticket_details.claimant.discord_id if ticket_details.claimant else None
        )
        if not claimant_id:
            return

        # there was a claimant, let them know ticket was canceled
        user = client.get_user(int(claimant_id))  # cache only
        if not user:
            user = await client.fetch_user(int(claimant_id))  # network request
        if not user:
            return

        try:
            await user.send(DMs.TICKET_CANCELED.format(mention=user.mention))
        except Exception:
            logger.exception("Failed to notify mentor of ticket cancelation")

    @staticmethod
    async def delete_ticket_message(ticket_details: TicketUpdate):
        try:
            message = await TicketMessage.get_ticket_message(ticket_details)
            await message.delete()
            await TicketMessage._notify_claimant(ticket_details)

        except discord.NotFound:
            logger.info("Message already deleted")
        except Exception:
            logger.exception("Failed to delete message on ticket cancel")
