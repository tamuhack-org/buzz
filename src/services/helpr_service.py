import logging

import discord

from src.exceptions.custom_exceptions import ChannelNotFound, InvalidChannelType
from src.schemas import TicketDetails
from src.utils.bot import client
from src.utils.config import settings
from src.views.buttons import TicketButtons
from src.views.embeds import TicketEmbeds

logger = logging.getLogger(__name__)

class HelprService:
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

        await channel.send(content=mentor_ping, embed=embed, view=view)
        logger.info("Mentors pinged!")

        return { "status_code": 200, "message": "Message sent to mentors!" }
