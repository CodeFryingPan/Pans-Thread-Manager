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


# Get the env variables
test_channel = int(os.getenv("TEST_CHANNEL_ID"))
production_channel = int(os.getenv("PRODUCTION_CHANNEL_ID"))
thread_channels = [test_channel]

upvode_id = int(os.getenv("UPVOTE_ID"))
thread_emojis = [upvode_id]

insight_role = int(os.getenv("REACTION_ROLE_ID"))
thread_role = insight_role

token = os.getenv("DISCORD_TOKEN")


# Setup to run the app in debug mode
if __name__ == "__main__":
    bot = DiscordClient(thread_channels=thread_channels, thread_emojis=thread_emojis, thread_role = thread_role)
    bot.run(token)
