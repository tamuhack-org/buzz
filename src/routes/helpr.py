from fastapi import APIRouter, Depends

from src.deps import RoleServiceDep, TicketServiceDep
from src.schemas import TicketDetails, TicketUpdate, UpdateRole
from src.utils.crypto import verify_hmac

router = APIRouter(
    prefix="/helpr",
    tags=["helpr"],
    dependencies=[Depends(verify_hmac)],
)


@router.post("/ping-mentor")
async def ping_mentor(
    ticket_details: TicketDetails,
    ticket_service: TicketServiceDep,
):
    return await ticket_service.post_ticket(ticket_details)


@router.post("/update-ticket")
async def update_ticket(ticket_details: TicketUpdate, ticket_service: TicketServiceDep):
    return await ticket_service.refresh_ticket(ticket_details)


@router.post("/cancel-ticket")
async def cancel_ticket(ticket_details: TicketUpdate, ticket_service: TicketServiceDep):
    return await ticket_service.cancel_ticket(ticket_details)


# NOTE: hmac verification only works on body so give pydantic object
@router.post("/give-role")
async def give_role(update_role: UpdateRole, role_service: RoleServiceDep):
    return await role_service.give_role(**update_role.model_dump())
