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
    WELCOME = (
        "Howdy {mention}!\n"
        "You'll now be alerted when there's a new help ticket.\n"
        "When you're done with your shift you can simply run /checkout in the server (or here) to stop receiving notifications.\n"
        "Thank you again for mentoring and we hope you have fun! "
    )
    NOT_IN_SERVER = (
        "You need to be in the TAMUhack server to get help ticket alerts.\n"
        "You can join here:\n"
        # TODO: generate dynamic link from settings.SERVER_ID?
        "https://discord.com/invite/fTTq42Qsz5"
    )
    TICKET_CANCELED = "Howdy {mention},\nYour current ticket was canceled."


class FollowUps:
    GENERIC_ERROR = f"Something went wrong\nPlease claim directly from [helpr]({settings.HELPR_URL})"
    DISCORD_NOT_LINKED = (
        "Your Helpr account isn't linked to Discord!\n"
        f"[Link your Discord]({settings.HELPR_URL}/link/discord)"
    )
    HAS_EXISTING_TICKET = (
        "You already have an active ticket. Mark it as finished or unclaim it first.\n"
        f"[Manage your tickets]({settings.HELPR_URL})"
    )
    TICKET_ALREADY_CLAIMED = "This ticket has already been claimed."
    TICKET_MISMATCH = (
        "You can't edit a ticket you haven't claimed. No changes were made.\n"
        f"[Manage your tickets]({settings.HELPR_URL})"
    )


class Checkout:
    NOT_MENTOR = "You're not a mentor.\nThis command is reserved for mentors."
    NOT_USER = "Only a discord user can run this command."
    NOT_FOUND = (
        "We could not find you in the server. Are you sure you're part of the server?"
    )
    ERROR = "Something went wrong.\nPlease contact an organizer to checkout"
    SUCCESS = "Successfully checked out.\nThanks for mentoring!\nNote: You still need to checkout with an organizer before leaving the venue"
