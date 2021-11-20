from src.clients.discord_client import DiscordClient
import os

# Import settings from .env file
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        os.environ[var[0]] = var[1]

# Get the mode
token = os.getenv("DISCORD_TOKEN")

# Setup to run the app in debug mode
if __name__ == "__main__":
    bot = DiscordClient()
    bot.run(token)
