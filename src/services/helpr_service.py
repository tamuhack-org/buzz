import logging

import discord

from src.exceptions.custom_exceptions import ChannelNotFound, InvalidChannelType, MessageNotFound
from src.schemas import TicketDetails, TicketUpdate
from src.utils.bot import client
from src.utils.config import settings
from src.views.buttons import TicketButtons
from src.views.embeds import TicketEmbeds

logger = logging.getLogger(__name__)


class HelprService:
    async def _get_ticket_message(
        self, ticket: TicketUpdate
    ) -> discord.Message:
        channel_id = int(ticket.channel_id)
        message_id = int(ticket.message_id)
        #looks up local cache
        channel = client.get_channel(channel_id)
        if channel is None:
            #http request
            channel = await client.fetch_channel(channel_id)

        if channel is None or not isinstance(channel, discord.TextChannel):
            raise InvalidChannelType("text channel", ticket.channel_id)

        message = await channel.fetch_message(message_id)
        if not message:
            raise MessageNotFound(ticket.message_id, ticket.channel_id)

        return message

    async def ping_mentor(self, ticket_details: TicketDetails):
        logger.info("Attemping to ping mentors")
        channel = client.get_channel(settings.MENTOR_CHANNEL_ID)
        if not channel:
            logger.info("Provided mentor channel ID not found")
            raise ChannelNotFound(str(settings.MENTOR_CHANNEL_ID))

        if not isinstance(channel, (discord.TextChannel)):
            logger.info("Provided mentor channel is not a text channel")
            raise InvalidChannelType("text channel", str(settings.MENTOR_CHANNEL_ID))

        mentor_ping = f"<@&{settings.MENTOR_ROLE_ID}>"
        embed = TicketEmbeds.ticket_created(ticket_details)
        view = TicketButtons(ticket_details)

        message = await channel.send(content=mentor_ping, embed=embed, view=view)
        message_info = {
            "channel_id": str(message.channel.id),
            "message_id": str(message.id)
        }

        logger.info("Mentors pinged!")

        return {
            "status_code": 200,
            "message": "Message sent to mentors!",
            "message_info": message_info,
        }
