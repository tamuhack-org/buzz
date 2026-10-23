from typing import Annotated

from fastapi import Depends

from src.services.role_service import RoleService
from src.services.ticket_service import TicketService


async def get_ticket_service() -> TicketService:
    return TicketService()

async def get_role_service() -> RoleService:
    return RoleService()

TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
RoleServiceDep = Annotated[RoleService, Depends(get_role_service)]
