from src.clients.discord_client import DiscordClient
import os
import sys
import json

from src.clients.discord_clientV2 import DiscordClientV2

# Import settings from .env file
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        os.environ[var[0]] = var[1]
else:
    print("ERROR: .env file does not exist failing the script.")
    sys.exit("FAILED TO RUN SCRIPT MISSING .env")

token = os.getenv("DISCORD_TOKEN")

# Setup to run the app in debug mode
if __name__ == "__main__":
    if os.path.exists('channels.json'):
        f = open('channels.json')
        threads = json.load(f)

        bot = DiscordClientV2(threads=threads["channels"])
        bot.run(token)
    else:
        print("ERROR: channels.json file does not exist failing the script.")
        sys.exit("FAILED TO RUN SCRIPT MISSING channels.json")