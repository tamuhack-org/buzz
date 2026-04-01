from fastapi import APIRouter, Request
from src.deps import HelprDep 

router = APIRouter(
    prefix="/helpr",
    tags=["helpr"],
)

#TODO: Need to add some kinda authentication
@router.get("/ping-mentor")
async def ping_mentor( request: Request, service: HelprDep, ):
    return await service.ping_mentor()

