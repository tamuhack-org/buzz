import discord

from src.exceptions.custom_exceptions import BadRequest
from src.schemas import TicketDetails, TicketUpdate, UpdateRole
from src.views.manage_message import TicketMessage
from src.utils.bot import BotStuff
from src.utils.config import settings


class HelprService:
    async def ping_mentor(self, ticket_details: TicketDetails):
        return await TicketMessage.create_ticket_message(ticket_details)

    async def update_ticket(self, ticket_details: TicketUpdate):
        return await TicketMessage.update_ticket_message(ticket_details)

    async def cancel_ticket(self, ticket_details: TicketUpdate):
        return await TicketMessage.delete_ticket_message(ticket_details)

    async def give_mentor_role(self, update_role: UpdateRole):
        return await BotStuff.give_role(role_id=settings.MENTOR_ROLE_ID, user_id=update_role.user_id, server_id=update_role.server_id)
