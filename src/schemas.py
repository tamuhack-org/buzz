from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


class HelprModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)


class User(HelprModel):
    name: str
    email: str
    user_id: str = Field(alias="id")
    is_mentor: bool = Field(alias="mentor")
    discord_id: str | None = Field(default=None, alias="discordId")


# TODO: Add aliases to match buzz responses
class TicketDetails(HelprModel):
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
    channel_id: str = Field(alias="discordChannelId")
    message_id: str = Field(alias="discordMessageId")
