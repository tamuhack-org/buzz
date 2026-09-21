from fastapi import APIRouter, Depends

from src.deps import Helpr
from src.schemas import TicketDetails
from src.utils.crypto import verify_hmac

router = APIRouter(
    prefix="/helpr",
    tags=["helpr"],
    dependencies=[Depends(verify_hmac)],
)

@router.post("/ping-mentor")
async def ping_mentor( ticket_details: TicketDetails, service: Helpr, ):
    return await service.ping_mentor(ticket_details)
