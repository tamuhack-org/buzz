import enum
import json
import logging

import httpx

from src.bot.strings import FollowUps
from src.schemas import TicketUpdate
from src.utils.config import settings
from src.utils.crypto import create_hmac

logger = logging.getLogger(__name__)


class HelprError(enum.StrEnum):
    DISCORD_NOT_LINKED = FollowUps.DISCORD_NOT_LINKED
    HAS_EXISTING_TICKET = FollowUps.HAS_EXISTING_TICKET
    TICKET_ALREADY_CLAIMED = FollowUps.TICKET_ALREADY_CLAIMED
    TICKET_MISMATCH = FollowUps.TICKET_MISMATCH


class HelprApiError(Exception):
    """code is set when helpr returned a known error code, None for anything unexpected."""

    def __init__(self, code: HelprError | None, detail: str = "") -> None:
        super().__init__(detail or str(code))
        self.code = code


_http = httpx.AsyncClient(base_url=settings.HELPR_URL, timeout=10)


async def close() -> None:
    await _http.aclose()


async def post_ticket_action(
    action: str, *, discord_id: str, ticket_id: str
) -> TicketUpdate:
    body = json.dumps({"discordId": discord_id, "ticketId": ticket_id}, separators=(",", ":"))
    headers = create_hmac(body) | {"Content-Type": "application/json"}

    try:
        response = await _http.post(
            f"/api/tickets/{action}", content=body, headers=headers
        )
    except httpx.HTTPError as err:
        raise HelprApiError(None, str(err)) from err

    try:
        data = response.json()
    except ValueError:
        data = {}

    code = data.get("code")
    if isinstance(code, str) and code in HelprError.__members__:
        raise HelprApiError(HelprError[code])
    if response.status_code != 200:
        raise HelprApiError(
            None, f"{action} failed ({response.status_code}): {response.text}"
        )

    return TicketUpdate.model_validate(data["ticket"])
