import asyncio
import discord
import uvicorn
from fastapi import FastAPI

class App:

    def __init__(self) -> None:
        pass

app = FastAPI()
bot = discord.Client()