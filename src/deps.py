from typing import Annotated

from fastapi import Depends

from src.services.helpr_service import HelprService


async def get_helpr_service() -> HelprService:
    return HelprService()

Helpr = Annotated[HelprService, Depends(get_helpr_service)]
