import discord
from src.schemas import TicketDetails

class TicketEmbeds:
    @staticmethod
    def ticket_created(ticket_details: TicketDetails):
        embed = discord.Embed(
            title="New Ticket!",
            description=f"**Issue:** {ticket_details.issue}",
            color=discord.Color.purple(),
            timestamp=ticket_details._created_at
        )

        embed.add_field(name="👩🏻‍💻 Hacker", value=ticket_details.name, inline=True)
        embed.add_field(name="📍 Location", value=f"`{ticket_details.location}`", inline=True)
        embed.add_field(name="📞 Contact", value=ticket_details.phone_number, inline=False)

        embed.set_footer(text="Helpr")

        return embed
