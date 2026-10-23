from typing import Annotated

from fastapi import Depends

from src.services.ticket_service import TicketService
from src.services.role_service import RoleService


async def get_ticket_service() -> TicketService:
    return TicketService()

async def get_role_service() -> RoleService:
    return RoleService()

Tickets = Annotated[TicketService, Depends(get_ticket_service)]
Roles = Annotated[RoleService, Depends(get_role_service)]
