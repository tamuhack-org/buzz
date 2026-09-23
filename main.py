# TODO: State is very unidirectional. It only goes buzz -> helpr. If changes happen on helpr, buzz should be able to pick up on that.

import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routes import helpr
from src.utils.bot import client
from src.utils.config import settings

LOG_LEVEL = settings.LOG_LEVEL.upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s:  %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    #use asyncio to spin up new task because client.start runs infinitely
    asyncio.create_task(client.start(settings.DISCORD_BOT_TOKEN))
    yield
    await client.close()

app = FastAPI(lifespan=lifespan)

app.include_router(helpr.router)
