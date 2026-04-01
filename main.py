import discord
from fastapi import FastAPI
from src.routes import helpr

app = FastAPI()

app.include_router(helpr.router)
