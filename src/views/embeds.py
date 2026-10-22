import discord

from src.bot.strings import Embeds
from src.schemas import TicketDetails


class TicketEmbeds:
    @staticmethod
    def generic_ticket(
        ticket_details: TicketDetails,
        color: discord.Color | None = None,
        footer_text: str = Embeds.FOOTER_DEFAULT,
    ) -> discord.Embed:
        if color is None:
            color = discord.Color.blurple()

        embed = discord.Embed(
            title=Embeds.TITLE,
            description=Embeds.ISSUE.format(issue=ticket_details.issue),
            color=color,
            timestamp=ticket_details.created_at,
        )

        embed.add_field(
            name=Embeds.FIELD_HACKER, value=ticket_details.author.name, inline=True
        )
        embed.add_field(
            name=Embeds.FIELD_LOCATION, value=ticket_details.location, inline=True
        )
        embed.add_field(
            name=Embeds.FIELD_CONTACT, value=ticket_details.phone_number, inline=False
        )

        embed.set_footer(text=footer_text)

        return embed

    @staticmethod
    def ticket_available(ticket_details: TicketDetails) -> discord.Embed:
        return TicketEmbeds.generic_ticket(
            ticket_details, discord.Color.purple(), Embeds.FOOTER_AVAILABLE
        )

    @staticmethod
    def ticket_claimed(ticket_details: TicketDetails) -> discord.Embed:
        if not ticket_details.claimant:
            return TicketEmbeds.ticket_error(ticket_details)

        return TicketEmbeds.generic_ticket(
            ticket_details,
            discord.Color.gold(),
            Embeds.FOOTER_CLAIMED.format(claimant_name=ticket_details.claimant.name),
        )

    @staticmethod
    def ticket_resolved(ticket_details: TicketDetails) -> discord.Embed:
        if not ticket_details.claimant:
            return TicketEmbeds.ticket_error(ticket_details)

        return TicketEmbeds.generic_ticket(
            ticket_details,
            discord.Color.green(),
            Embeds.FOOTER_RESOLVED.format(claimant_name=ticket_details.claimant.name),
        )

    # generic catch all error
    @staticmethod
    def ticket_error(ticket_details: TicketDetails) -> discord.Embed:
        return TicketEmbeds.generic_ticket(
            ticket_details, discord.Color.green(), Embeds.FOOTER_ERROR
        )
