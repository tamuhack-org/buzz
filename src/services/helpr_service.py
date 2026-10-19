from src.schemas import TicketDetails, TicketUpdate
from src.views.manage_message import TicketMessage

class HelprService:
    async def ping_mentor(self, ticket_details: TicketDetails):
        return await TicketMessage.create_ticket_message(ticket_details)

    async def update_ticket(self, ticket_details: TicketUpdate):
        return await TicketMessage.update_ticket_message(ticket_details)

    async def cancel_ticket(self, ticket_details: TicketUpdate):
        return await TicketMessage.delete_ticket_message(ticket_details)
