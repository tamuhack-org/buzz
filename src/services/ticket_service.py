import logging

import discord
from fastapi import HTTPException

from src.bot.client import client
from src.bot.render import render_ticket
from src.bot.strings import DMs
from src.clients import helpr_client
from src.exceptions.custom_exceptions import (
    ChannelNotFound,
    InternalServerError,
    InvalidChannelType,
    MessageNotFound,
)
from src.schemas import TicketDetails, TicketState, TicketUpdate
from src.utils.config import settings

logger = logging.getLogger(__name__)


# TODO: look into what should remain in views and what should go in a templates fodler
class TicketService:
    async def apply_action(
        self, action: str, *, ticket_id: str, discord_id: str, message: discord.Message
    ) -> None:
        updated = await helpr_client.post_ticket_action(
            action, discord_id=discord_id, ticket_id=ticket_id
        )
        await self.refresh_ticket(updated, message)

    async def _get_message(self, ticket: TicketUpdate) -> discord.Message:
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

    async def post_ticket(self, ticket: TicketDetails):
        logger.info("Attemping to ping mentors")
        channel = client.get_channel(settings.MENTOR_CHANNEL_ID)
        if not channel:
            logger.info("Provided mentor channel ID not found")
            raise ChannelNotFound(str(settings.MENTOR_CHANNEL_ID))

        if not isinstance(channel, (discord.TextChannel)):
            logger.info("Provided mentor channel is not a text channel")
            raise InvalidChannelType("text channel", str(settings.MENTOR_CHANNEL_ID))

        rendered_message = render_ticket(ticket)
        message = await channel.send(**rendered_message.as_kwargs())

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

    async def refresh_ticket(
        self, ticket: TicketUpdate, message: discord.Message | None = None
    ) -> None:
        if message is None:
            message = await self._get_message(ticket)

        await message.edit(**render_ticket(ticket).as_kwargs())

        if ticket.state() == TicketState.ERROR:
            raise HTTPException(status_code=422, detail="ticket state inconsistent")

    # TODO: maybe move to a dedicated dm method?
    async def _notify_claimant(self, ticket_details: TicketUpdate):
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

    async def cancel_ticket(self, ticket_details: TicketUpdate):
        try:
            message = await self._get_message(ticket_details)
            await message.delete()
            await self._notify_claimant(ticket_details)

        except discord.NotFound:
            logger.info("Message already deleted")
        except Exception:
            logger.exception("Failed to delete message on ticket cancel")
            raise InternalServerError("Failed to delete message on ticket cancel")
