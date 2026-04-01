from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/helpr",
    tags=["helpr"],
)

@router.get("/test")
async def test(
    request: Request,
):
    return "hi"

