from src.utils.bot import client
from src.exceptions.custom_exceptions import ChannelNotFound
from src.schemas import TicketDetails
from src.embeds import TicketEmbeds
from src.utils.config import settings

class HelprService():
    async def ping_mentor(self, ticket_details: TicketDetails):
        channel = client.get_channel(settings.MENTOR_CHANNEL_ID)
        if not channel:
            raise ChannelNotFound(str(settings.MENTOR_CHANNEL_ID))

        mentor_ping = f"<@&{settings.MENTOR_ROLE_ID}>"
        embed = TicketEmbeds.ticket_created(ticket_details)

        await channel.send(content=mentor_ping, embed=embed)
        return { "status_code": 200, "message": "Message sent to mentors!" }
