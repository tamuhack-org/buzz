from dataclasses import dataclass

import discord

from src.bot.strings import Embeds, Messages
from src.schemas import TicketDetails, TicketState, User
from src.utils.config import settings
from src.views.buttons import TicketButtons  # replaced in step 6


@dataclass
class RenderedTicket:
    content: str
    embed: discord.Embed
    view: discord.ui.View

    # NOTE: just prevents a deep copy which is default with dataclass
    def as_kwargs(self) -> dict:
        return {"content": self.content, "embed": self.embed, "view": self.view}


def _display_name(user: User) -> str:
    return f"<@{user.discord_id}>" if user.discord_id else user.name


def _embed(ticket: TicketDetails, color: discord.Color, footer: str) -> discord.Embed:
    if color is None:
        color = discord.Color.blurple()

    embed = discord.Embed(
        title=Embeds.TITLE,
        description=Embeds.ISSUE.format(issue=ticket.issue),
        color=color,
        timestamp=ticket.created_at,
    )

    embed.add_field(name=Embeds.FIELD_HACKER, value=ticket.author.name, inline=True)
    embed.add_field(name=Embeds.FIELD_LOCATION, value=ticket.location, inline=True)
    embed.add_field(name=Embeds.FIELD_CONTACT, value=ticket.phone_number, inline=False)

    embed.set_footer(text=footer)
    return embed


def render_ticket(ticket: TicketDetails) -> RenderedTicket:
    state = ticket.state()
    view = TicketButtons(ticket, state)
    claimant = ticket.claimant

    # TODO: Switch cases :D
    # TODO: Consider moving ribbon colors to a more easily editable place?
    if state == TicketState.RESOLVED and claimant:
        return RenderedTicket(
            content=Messages.TICKET_RESOLVED.format(claimant=_display_name(claimant)),
            embed=_embed(
                ticket,
                discord.Color.green(),
                Embeds.FOOTER_RESOLVED.format(claimant_name=claimant.name),
            ),
            view=view,
        )

    elif state == TicketState.CLAIMED and claimant:
        return RenderedTicket(
            content=Messages.TICKET_CLAIMED.format(claimant=_display_name(claimant)),
            embed=_embed(
                ticket,
                discord.Color.gold(),
                Embeds.FOOTER_CLAIMED.format(claimant_name=claimant.name),
            ),
            view=view,
        )

    elif state == TicketState.AVAILABLE:
        return RenderedTicket(
            content=Messages.TICKET_AVAILABLE.format(
                mentor_role_id=settings.MENTOR_ROLE_ID
            ),
            embed=_embed(ticket, discord.Color.purple(), Embeds.FOOTER_AVAILABLE),
            view=view,
        )

    return RenderedTicket(
        content=Messages.TICKET_ERROR,
        embed=_embed(ticket, discord.Color.red(), Embeds.FOOTER_ERROR),
        view=view,
    )
