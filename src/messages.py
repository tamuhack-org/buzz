import inspect
from src.schemas import TicketDetails
from src.utils.config import settings

class TicketMessages:
    @staticmethod
    def ticket_created(ticket_details: TicketDetails) -> str:
        message = f"""<@&{settings.MENTOR_ROLE_ID}>
        There's a new ticket from **{ticket_details.name}**!
        They want to know: 
        ```{ticket_details.issue}``` 
        They're located **{ticket_details.location}** 
        You can reach them at **{ticket_details.phone_number}** or **{ticket_details.email}**."""

        return inspect.cleandoc(message) #remove leading whitespaces
