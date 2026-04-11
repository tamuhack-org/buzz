import time
import hashlib
import hmac
from fastapi import Request
from fastapi import Depends
from typing import Annotated
from src.services.helpr_service import HelprService
from src.utils.config import settings
from src.exceptions.custom_exceptions import Unauthorized


async def get_helpr_service() -> HelprService:
    return HelprService()

async def verify_hmac(request: Request):
    if settings.ENV == "development":
        return

    request_hmac = request.headers.get('X-Authorization-Content-HMAC')
    request_timestamp = request.headers.get('X-Authorization-Timestamp')

    if not request_hmac:
        raise Unauthorized("Missing HMAC signature header")

    if not request_timestamp:
        raise Unauthorized("Missing HMAC timestamp header")

    #make sure request is not older than 5 min
    if abs(time.time() - float(request_timestamp)) > 300:
        raise Unauthorized("Provided HMAC timestamp is either too old or invalid")

    request_body_raw = await request.body()
    request_body = request_body_raw.decode('utf-8')
    msg = f"{request_timestamp}{request_body}".encode('utf-8')

    new_hmac = hmac.new(key=settings.HMAC_SECRET.encode('utf-8'), msg=msg, digestmod=hashlib.sha256).hexdigest()

    if not hmac.compare_digest(request_hmac, new_hmac):
        raise Unauthorized("HMAC Signature Does not match")


Helpr = Annotated[HelprService, Depends(get_helpr_service)]
