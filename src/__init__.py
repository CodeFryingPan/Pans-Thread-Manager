from faulthandler import is_enabled
from fastapi import FastAPI
from src.clients.discord_client import DiscordClient
import os

def create_app(config_name, threads):
    """
    This will create an instance of FastAPI with the specified routers
    :param config_name: Setup the config name
    :return: A FastAPI Instance
    """

    # TODO: Setup these clients in the clients folder instead of here.
    # NEED TO SPECIFY Thread channels and thread_emojis
    bot = DiscordClient(threads = threads)

    from src.config.config import config
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

    return app, bot