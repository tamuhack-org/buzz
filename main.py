import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from clients import helpr_client
from src.routes import helpr
from src.utils.config import settings
from src.bot.client import client
from src.bot.commands import checkout

LOG_LEVEL = settings.LOG_LEVEL.upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(levelname)s:  %(asctime)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.tree.add_command(checkout)
    # NOTE: use asyncio to spin up new task because client.start runs infinitely
    # keep reference so its not garbage collected
    bot_task = asyncio.create_task(client.start(settings.DISCORD_BOT_TOKEN))
    yield
    await client.close()
    await helpr_client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(helpr.router)
