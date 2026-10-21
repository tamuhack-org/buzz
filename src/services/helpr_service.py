import discord

from src.exceptions.custom_exceptions import BadRequest
from src.schemas import TicketDetails, TicketUpdate
from src.views.manage_message import TicketMessage
from src.utils.bot import BotStuff


class HelprService:
    async def ping_mentor(self, ticket_details: TicketDetails):
        return await TicketMessage.create_ticket_message(ticket_details)

    async def update_ticket(self, ticket_details: TicketUpdate):
        return await TicketMessage.update_ticket_message(ticket_details)

    async def cancel_ticket(self, ticket_details: TicketUpdate):
        return await TicketMessage.delete_ticket_message(ticket_details)

    async def give_role(self, *, role_id: int, user_id: int, server_id: int):
        return await BotStuff.give_role(role_id=role_id, user_id=user_id, server_id=server_id)
