import discord

class TicketButtons(discord.ui.View):
    def __init__(self, ticket_details):
        timeout = 172800 #timeout in 2 days
        super().__init__(timeout=timeout)
        self.ticket_details = ticket_details
        self.add_item(discord.ui.Button(
            label="View Ticket",
            url="https://helpr.tamuhack.org/mentor",
        ))

    #@discord.ui.button(label="View Ticket", style=discord.ButtonStyle.blurple)
    #async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
    #    await interaction.response.edit_message(view=self)
