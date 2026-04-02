from datetime import datetime, timezone
from pydantic import BaseModel

class TicketDetails(BaseModel):
    name: str
    email: str
    location: str
    #might wanna change to pydantic's phone number type
    #but rn helpr is too loose with numbers and we don't want things breaking bcuz of that
    phone_number: str 
    issue: str
    _created_at: datetime = datetime.now(timezone.utc)

