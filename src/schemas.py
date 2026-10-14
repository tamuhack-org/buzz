from datetime import UTC, datetime

from pydantic import BaseModel


class User(BaseModel):
    name: str
    email: str
    user_id: str
    is_mentor: bool
    discord_id: str | None = None


class TicketDetails(BaseModel):
    author: User
    claimant: User | None = None
    location: str
    # TODO: might wanna change to pydantic's phone number type
    # but rn helpr is too loose with numbers and we don't want things breaking bcuz of that
    phone_number: str
    issue: str
    ticket_id: str
    resolved: bool
    _created_at: datetime = datetime.now(UTC)
