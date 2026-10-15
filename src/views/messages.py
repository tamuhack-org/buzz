from src.exceptions.custom_exceptions import BadRequest
from src.schemas import TicketDetails
from src.utils.config import settings


class TicketMessages:
    @staticmethod
    def ticket_available(ticket_details: TicketDetails) -> str:
        return f"<@&{settings.MENTOR_ROLE_ID}>"

    @staticmethod
    def ticket_claimed(ticket_details: TicketDetails) -> str:
        if ticket_details.claimant is None:
            raise BadRequest("Ticket does not have a claimant")

        if ticket_details.claimant.discord_id is not None:
            return f"Ticket claimed by <@&{ticket_details.claimant.discord_id}"

        # just use name as fallback
        return f"Ticket claimed by {ticket_details.claimant.name}"

    @staticmethod
    def ticket_resolved(ticket_details: TicketDetails) -> str:
        if not ticket_details.resolved:
            raise BadRequest("Ticket has not been resolved yet")

        if ticket_details.claimant is None:
            raise BadRequest("Ticket does not have a claimant")

        if ticket_details.claimant.discord_id is not None:
            return f"Ticket resolved by <@&{ticket_details.claimant.discord_id}"

        # just use name as fallback
        return f"Ticket resolved by {ticket_details.claimant.name}"

    @staticmethod
    def ticket_error(ticket_details: TicketDetails) -> str:
        return f"Something went wrong, please handle from helpr directly [helpr]({settings.HELPR_URL})"
