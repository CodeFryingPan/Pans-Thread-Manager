from src.clients.discord_client import DiscordClient
import os
import sys
import json

from src.clients.discord_clientV2 import DiscordClientV2

is_prod = os.environ.get('IS_HEROKU', None)

if not is_prod:
    # Import settings from .env file while development
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
if __name__ == "__main__" and not is_prod:
    if os.path.exists('channels.json'):
        f = open('channels.json')
        threads = json.load(f)

        bot = DiscordClientV2(threads=threads["channels"])
        bot.run(token)
    else:
        print("ERROR: channels.json file does not exist failing the script.")
        sys.exit("FAILED TO RUN SCRIPT MISSING channels.json")

# Setup to run the app in production mode
if __name__ == "__main__" and is_prod:
    threads = json.loads(os.getenv("CHANNELS_JSON"))

    print(threads)
    
    bot = DiscordClientV2(threads=threads["channels"])
    
    print("BOT OBJECT CREATED SUCCESSFULLY --- RUNNING BOT")
    
    bot.run(token)