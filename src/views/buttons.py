import logging
import httpx
import discord
from src.schemas import TicketDetails
from src.utils.config import settings
from src.utils.crypto import create_hmac

logger = logging.getLogger(__name__)

class TicketButtons(discord.ui.View):
    def __init__(self, ticket_details: TicketDetails):
        timeout = 172800 #timeout in 2 days
        super().__init__(timeout=timeout)
        self.ticket_details = ticket_details

        self.add_item(discord.ui.Button(
            label="View Ticket",
            url=f"{settings.HELPR_URL}/mentor",
        ))

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        userId = str(interaction.user.id)
        ticketId = self.ticket_details.ticketId
        logger.debug(f"Attemping to claim ticket: {ticketId} for user: {userId}")

        await interaction.response.defer(ephemeral=True)

        url = f"{settings.HELPR_URL}/api/tickets/claim"
        payload = { "discordId": userId, "ticketId": ticketId }
        headers = create_hmac(payload)

        #TODO: handle not linked
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            data = response.json()
            logger.info(f"Claim ticket post request result: {response.status_code}")

            if(data.get("code") == "DISCORD_NOT_LINKED"):
                #discord account not linked
                link_url = f"{settings.HELPR_URL}/link/discord"
                #send private followup with url to link account
                await interaction.followup.send(
                    content=f"Your helpr account isn't linked to your discord! [Click here to link your Discord]({link_url})",
                    ephemeral=True
                )
                return

            elif(response.status_code != 200):
                #generic failure message
                #TODO might not want to be a global edit?
                button.disabled = True
                if not interaction.message:
                    #if for some reason embed is missing
                    return

                embed = interaction.message.embeds[0]
                embed.color = discord.Color.red()
                await interaction.edit_original_response(content=f"Something went wrong. Please claim directly from [helpr]({settings.HELPR_URL})!")
                await interaction.message.edit(embed=embed, view=self)
                return

            #TODO add button to unclaim/resolve (only for claimed user)
            #success: mark as claimed and change embed of message
            button.label = "Claimed"
            button.style = discord.ButtonStyle.success
            button.disabled = True

            if not interaction.message:
                #if for some reason embed is missing
                return

            embed = interaction.message.embeds[0]
            embed.set_footer(text=f"Claimed by {interaction.user.display_name}")
            embed.color = discord.Color.green()

        #edits actual message
        await interaction.edit_original_response(content="Ticket claimed!", view=None)
        #edits embed
        await interaction.message.edit(embed=embed, view=self)
