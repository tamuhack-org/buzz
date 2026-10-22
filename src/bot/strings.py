# holds all user facing strings/text


from src.utils.config import settings


class Buttons:
    VIEW = "View Ticket"
    CLAIM = "Claim Ticket"
    UNCLAIM = "Unclaim Ticket"
    RESOLVE = "Resolve Ticket"


class Embeds:
    TITLE = "New Ticket!"
    ISSUE = "**Issue:** {issue}"
    FIELD_HACKER = "👩🏻‍💻 Hacker"
    FIELD_LOCATION = "📍 Location"
    FIELD_CONTACT = "📞 Contact"
    FOOTER_DEFAULT = "Helpr"
    FOOTER_AVAILABLE = "Helpr"
    FOOTER_CLAIMED = "Claimed by {claimant_name}"
    FOOTER_RESOLVED = "Resolved by {claimant_name}"
    FOOTER_ERROR = "Helpr"


class Messages:
    TICKET_AVAILABLE = "<@&{mentor_role_id}>"
    TICKET_CLAIMED = "Ticket claimed by {claimant}"
    TICKET_RESOLVED = "Ticket resolved by {claimant}"
    TICKET_ERROR = f"Something went wrong, please handle from helpr directly [helpr]({settings.HELPR_URL})"


class DMs:
    TICKET_CANCELED = "Howdy {discord_id},\nYour current ticket was canceled."


class FollowUps:
    GENERIC_ERROR = (
        f"Something went wrongPlease claim directly from [helpr]({settings.HELPR_URL})"
    )
    DISCORD_NOT_LINKED = (
        "Your Helpr account isn't linked to Discord! "
        f"[Link your Discord]({settings.HELPR_URL}/link/discord)"
    )
    HAS_EXISTING_TICKET = (
        "You already have an active ticket. Mark it as finished or unclaim it first. "
        f"[Manage your tickets]({settings.HELPR_URL})"
    )
    TICKET_ALREADY_CLAIMED = "This ticket has already been claimed."
    TICKET_MISMATCH = (
        "You can't edit a ticket you haven't claimed. No changes were made. "
        f"[Manage your tickets]({settings.HELPR_URL})"
    )


class Checkout:
    NOT_MENTOR = "You're not a mentor.\nThis command is reserved for mentors."
    NOT_USER = "Only a discord user can run this command."
    ERROR = "Something went wrong.\nPlease contact an organizer to checkout"
    SUCCESS = "Succesfully checked out.\nThanks for mentoring!\nNote: You still need to checkout with an organizer before leaving the venue"
