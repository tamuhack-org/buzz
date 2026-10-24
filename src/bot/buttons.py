import logging

import discord

from src.bot.strings import FollowUps
from src.clients.helpr_client import HelprApiError
from src.schemas import TicketAction
from src.services.ticket_service import TicketService

logger = logging.getLogger(__name__)


_action_pattern = "|".join(action.value for action in TicketAction)


class TicketActionButton(
    discord.ui.DynamicItem[discord.ui.Button],
    # template=rf"buzz:(?P<action>{_action_pattern}):(?P<ticket_id>.+)",
    template=r"buzz:(?P<action>claim|unclaim|resolve):(?P<ticket_id>.+)",
):
    def __init__(self, action: TicketAction, ticket_id: str) -> None:
        super().__init__(discord.ui.Button(custom_id=f"buzz:{action}:{ticket_id}"))
        self.action = action
        self.ticket_id = ticket_id

    @classmethod
    async def from_custom_id(cls, interaction, item, match):
        return cls(TicketAction(match["action"]), match["ticket_id"])

    async def callback(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(ephemeral=True)
        except discord.NotFound:
            logger.warning(
                f"{self.action} on ticket {self.ticket_id} expired before it could be acknowledged"
            )
            return
        if interaction.message is None:
            await interaction.followup.send(FollowUps.GENERIC_ERROR, ephemeral=True)
            return

        try:
            await TicketService().apply_action(
                self.action,
                ticket_id=self.ticket_id,
                discord_id=str(interaction.user.id),
                message=interaction.message,
            )
        except HelprApiError as err:
            if err.code is None:
                logger.error(str(err))
            await interaction.followup.send(
                str(err.code or FollowUps.GENERIC_ERROR), ephemeral=True
            )
        except Exception:
            logger.exception(f"{self.action} failed for ticket {self.ticket_id}")
            await interaction.followup.send(FollowUps.GENERIC_ERROR, ephemeral=True)
