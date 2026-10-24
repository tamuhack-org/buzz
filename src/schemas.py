from datetime import UTC, datetime
from enum import Enum, StrEnum

from pydantic import BaseModel, ConfigDict, Field


class HelprModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class User(HelprModel):
    name: str
    email: str
    user_id: str = Field(alias="id")
    is_mentor: bool = Field(alias="mentor")
    discord_id: str | None = Field(default=None, alias="discordId")


class TicketAction(StrEnum):
    CLAIM = "claim"
    UNCLAIM = "unclaim"
    RESOLVE = "resolve"


class TicketState(str, Enum):
    AVAILABLE = "available"
    CLAIMED = "claimed"
    RESOLVED = "resolved"
    ERROR = "error"


class TicketDetails(HelprModel):
    def state(self) -> TicketState:
        if self.resolved and self.claimant:
            return TicketState.RESOLVED
        elif self.claimant:
            return TicketState.CLAIMED
        if self.claimant is None:
            return TicketState.AVAILABLE
        # some kinda indeterminant state
        return TicketState.ERROR

    author: User
    claimant: User | None = None
    location: str
    # TODO: might wanna change to pydantic's phone number type
    # but rn helpr is too loose with numbers and we don't want things breaking bcuz of that
    phone_number: str = Field(alias="contact")
    issue: str
    ticket_id: str = Field(alias="id")
    resolved: bool = Field(alias="isResolved")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), alias="publishTime"
    )


class TicketUpdate(TicketDetails):
    # using both validation and serialization aliases for pyright to recognize field names
    channel_id: str = Field(
        validation_alias="discordChannelId", serialization_alias="discordChannelId"
    )
    message_id: str = Field(
        validation_alias="discordMessageId", serialization_alias="discordMessageId"
    )


class UpdateRole(BaseModel):
    role_id: int
    user_id: int
    server_id: int
