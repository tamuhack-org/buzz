import discord
import logging
from fastapi import HTTPException

from src.schemas import TicketDetails, TicketUpdate
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

        mentor_ping = f"<@&{settings.MENTOR_ROLE_ID}>"
        content = TicketMessages.ticket_available(ticket_details)
        embed = TicketEmbeds.ticket_available(ticket_details)
        view = TicketButtons(ticket_details)

        message = await channel.send(content=mentor_ping, embed=embed, view=view)
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
    async def update_ticket_message(ticket_details: TicketUpdate):
        message = await TicketMessage.get_ticket_message(ticket_details)
        if ticket_details.resolved and ticket_details.claimant is not None:
            content = TicketMessages.ticket_resolved(ticket_details)
            embed = TicketEmbeds.ticket_resolved(ticket_details)

        elif ticket_details.claimant and ticket_details.claimant.user_id is not None:
            content = TicketMessages.ticket_claimed(ticket_details)
            embed = TicketEmbeds.ticket_claimed(ticket_details)

        elif not ticket_details.claimant:
            content = TicketMessages.ticket_available(ticket_details)
            embed = TicketEmbeds.ticket_available(ticket_details)

        else:
            # some kinda indeterminant error state
            content = TicketMessages.ticket_available(ticket_details)
            embed = TicketEmbeds.ticket_available(ticket_details)
            await message.edit(
                content=content,
                embed=embed,
            )
            raise HTTPException(status_code=422, detail="ticket state inconsistent")

        await message.edit(
            content=content,
            embed=embed,
        )
