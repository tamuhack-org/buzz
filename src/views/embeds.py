import discord

from src.schemas import TicketDetails


class TicketEmbeds:
    @staticmethod
    def generic_ticket(
        ticket_details: TicketDetails,
        color: discord.Color = discord.Color.purple(),
        footer_text: str = "Helpr",
    ) -> discord.Embed:
        embed = discord.Embed(
            title="New Ticket!",
            description=f"**Issue:** {ticket_details.issue}",
            color=color,
            timestamp=ticket_details._created_at,
        )

        embed.add_field(
            name="👩🏻‍💻 Hacker", value=ticket_details.author.name, inline=True
        )
        embed.add_field(
            name="📍 Location", value=f"`{ticket_details.location}`", inline=True
        )
        embed.add_field(
            name="📞 Contact", value=ticket_details.phone_number, inline=False
        )

        embed.set_footer(text=footer_text)

        return embed

    @staticmethod
    def ticket_available(ticket_details: TicketDetails) -> discord.Embed:
        return TicketEmbeds.generic_ticket(
            ticket_details, discord.Color.purple(), "Helpr"
        )

    @staticmethod
    def ticket_claimed(ticket_details: TicketDetails) -> discord.Embed:
        if not ticket_details.claimant:
            return TicketEmbeds.ticket_error(ticket_details)

        return TicketEmbeds.generic_ticket(
            ticket_details,
            discord.Color.dark_teal(),
            f"Claimed by {ticket_details.claimant.name}",
        )

    @staticmethod
    def ticket_resolved(ticket_details: TicketDetails) -> discord.Embed:
        if not ticket_details.claimant:
            return TicketEmbeds.ticket_error(ticket_details)

        return TicketEmbeds.generic_ticket(
            ticket_details,
            discord.Color.green(),
            f"Resolved by {ticket_details.claimant.name}",
        )

    # generic catch all error
    @staticmethod
    def ticket_error(ticket_details: TicketDetails) -> discord.Embed:
        return TicketEmbeds.generic_ticket(
            ticket_details, discord.Color.green(), "Helpr"
        )
