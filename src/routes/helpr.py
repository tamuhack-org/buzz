from fastapi import APIRouter, Depends
from src.deps import Helpr, verify_hmac
from src.schemas import TicketDetails

router = APIRouter(
    prefix="/helpr",
    tags=["helpr"],
    dependencies=[Depends(verify_hmac)],
)

#TODO: Need to add some kinda authentication
@router.post("/ping-mentor")
async def ping_mentor( ticket_details: TicketDetails, service: Helpr, ):
    return await service.ping_mentor(ticket_details)
