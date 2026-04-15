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

    async def edit_interaction(self, interaction: discord.Interaction, *, edited_msg: str, embed_color: discord.Color | None = None, embed_footer: str = ""):
        if not interaction.message:
            #if for some reason embed is missing
            return

        embed = interaction.message.embeds[0]
        #set the optional edits
        if embed_color:
            embed.color = embed_color
        if embed_footer:
            embed.set_footer(text=embed_footer)

        #edits actual message
        await interaction.edit_original_response(content=edited_msg)
        #edits embed
        await interaction.message.edit(embed=embed, view=self)
        return

    @discord.ui.button(label="Claim Ticket", style=discord.ButtonStyle.blurple)
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
        userId = str(interaction.user.id)
        ticketId = self.ticket_details.ticketId
        logger.debug(f"Attemping to claim ticket: {ticketId} for user: {userId}")

        await interaction.response.defer(ephemeral=True) #let discord know this might take a while and not timeout

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
                await self.edit_interaction(interaction, edited_msg=f"Something went wrong. Please claim directly from [helpr]({settings.HELPR_URL})!", embed_color=discord.Color.red())
                return

            #TODO add button to unclaim/resolve (only for claimed user)
            #TODO BUG if claim fails because user already has a claimed ticket, buzz still shows success (might be bug in helpr tbh) 
            #success: mark as claimed and change embed of message
            button.label = "Claimed"
            button.style = discord.ButtonStyle.success
            button.disabled = True
            await self.edit_interaction(interaction, edited_msg="Ticket claimed!", embed_color=discord.Color.green(), embed_footer=f"Claimed by {interaction.user.display_name}")

