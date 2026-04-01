from src.utils.bot import client
from src.utils.config import settings

class HelprService():
    async def ping_mentor(self):
        channel = client.get_channel(settings.MENTOR_CHANNEL_ID)
        if channel:
            #roles need to be prefixed with &
            await channel.send("<@&1488761385667002439>\nThere's a new ticket!")
        else:
            return "Channel not found"

        return "sent"
