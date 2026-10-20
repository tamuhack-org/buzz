from src.bot.strings import Messages
from src.exceptions.custom_exceptions import BadRequest
from src.schemas import TicketDetails
from src.utils.config import settings


class TicketMessages:
    @staticmethod
    def ticket_available(ticket_details: TicketDetails) -> str:
        return Messages.TICKET_AVAILABLE.format(settings.MENTOR_ROLE_ID)

    @staticmethod
    def ticket_claimed(ticket_details: TicketDetails) -> str:
        # TODO: Considering creating subclasses in exceptions for NoClaimant, etc?
        if ticket_details.claimant is None:
            raise BadRequest("Ticket does not have a claimant")

        if ticket_details.claimant.discord_id is not None:
            return  Messages.TICKET_CLAIMED.format(f"<@{ticket_details.claimant.discord_id}>")

        # just use name as fallback
        return  Messages.TICKET_CLAIMED.format(ticket_details.claimant.name)

    @staticmethod
    def ticket_resolved(ticket_details: TicketDetails) -> str:
        if not ticket_details.resolved:
            raise BadRequest("Ticket has not been resolved yet")

        if ticket_details.claimant is None:
            raise BadRequest("Ticket does not have a claimant")

        if ticket_details.claimant.discord_id is not None:
            return  Messages.TICKET_RESOLVED.format(f"<@{ticket_details.claimant.discord_id}>")

        # just use name as fallback
        return  Messages.TICKET_RESOLVED.format(f"<@{ticket_details.claimant.name}>")

    @staticmethod
    def ticket_error(ticket_details: TicketDetails) -> str:
        return Messages.TICKET_ERROR.format(settings.HELPR_URL)
