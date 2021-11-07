from fastapi import FastAPI
import discord
from src.config.config import config
import os

def create_app(config_name):
    """
    This will create an instance of FastAPI with the specified routers
    :param config_name: Setup the config name
    :return: A FastAPI Instance
    """

    # TODO: Setup these clients in the clients folder instead of here.

    # TODO: Setup the discord bot
    bot = discord.Client()

    #TODO: Setup proper configurations for FASTAPI
    app_config = config[config_name]
    app = FastAPI(
        title=app_config.title,
        description=app_config.description,
        version=app_config.version,
        debug=app_config.debug
    )

    #TODO: Get the router from the main file and other files later on
    from src.routes import main

    app.include_router(main.router)

    return app