# holds all user facing strings/text


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
    TICKET_AVAILABLE = "<@{mentor_role_id}>"
    TICKET_CLAIMED = "Ticket claimed by {claimant}"
    TICKET_RESOLVED = "Ticket resolved by {claimant}"
    TICKET_ERROR = "Something went wrong, please handle from helpr directly [helpr]({helpr_url})"

class DMs:
    TICKET_CANCELED = "Howdy {discord_id},\nYour current ticket was canceled."
