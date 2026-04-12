import httpx
import discord
from src.schemas import TicketDetails
from src.utils.config import settings

class TicketButtons(discord.ui.View):
    def __init__(self, ticket_details: TicketDetails):
        timeout = 172800 #timeout in 2 days
        super().__init__(timeout=timeout)
        self.ticket_details = ticket_details

        self.add_item(discord.ui.Button(
            label="View Ticket",
            url="https://helpr.tamuhack.org/mentor",
        ))

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        userId = str(interaction.user.id)
        ticketId = self.ticket_details.ticketId
        url = f"{settings.HELPR_URL}/api/tickets/claim"
        payload = { "discordId": userId, "ticketId": ticketId }

        #TODO: handle not linked
        async with httpx.AsyncClient() as client:
            await client.post(url, json=payload)

        #TODO: update buttons
        #await interaction.response.edit_message(view=self)
