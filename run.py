from src.clients.discord_client import DiscordClient
import os
import sys

# Import settings from .env file
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        os.environ[var[0]] = var[1]
else:
    print("ERROR: .env file does not exist failing the script.")
    sys.exit("FAILED TO RUN SCRIPT MISSING .env")

# Get the mode
token = os.getenv("DISCORD_TOKEN")

# Setup to run the app in debug mode
if __name__ == "__main__":
    bot = DiscordClient()
    bot.run(token)
