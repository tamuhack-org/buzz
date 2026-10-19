from fastapi import APIRouter, Depends

from src.deps import Helpr
from src.schemas import TicketDetails, TicketUpdate
from src.utils.crypto import verify_hmac

router = APIRouter(
    prefix="/helpr",
    tags=["helpr"],
    dependencies=[Depends(verify_hmac)],
)

@router.post("/ping-mentor")
async def ping_mentor( ticket_details: TicketDetails, service: Helpr, ):
    return await service.ping_mentor(ticket_details)

@router.post("/update-ticket")
async def update_ticket( ticket_details: TicketUpdate, service: Helpr):
    return await service.update_ticket(ticket_details)

@router.post("/cancel-ticket")
async def cancel_ticket( ticket_details: TicketUpdate, service: Helpr):
    return await service.cancel_ticket(ticket_details)
