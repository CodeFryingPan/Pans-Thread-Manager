import asyncio
import os
import uvicorn
from src import create_app
import unittest

# Import settings from .env file
if os.path.exists(".env"):
    print("Importing environment from .env file")
    for line in open(".env"):
        var = line.strip().split("=")
        os.environ[var[0]] = var[1]

# Get the mode
mode = os.getenv("FAST_API_CONFIG") or "development"
token = os.getenv("DISCORD_TOKEN")
app, bot = create_app(mode, token)

# Runs the tests
def test():
    """
     Run the tests

    """

    api_tests = unittest.TestLoader().discover("./tests/api")
    unittest.TextTestRunner(verbosity=2).run(api_tests)

    int_tests = unittest.TestLoader().discover("./tests/integrations")
    unittest.TextTestRunner(verbosity=2).run(int_tests)

    unit_tests = unittest.TestLoader().discover("./tests/unit")
    unittest.TextTestRunner(verbosity=2).run(unit_tests)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(bot.start(token))
    await asyncio.sleep(4)
    print(f"{bot.user} has connected to Discord!")

@app.get("/user")
async def user():
    return {"User": "{}".format(bot.user)}

# Setup to run the app in debug mode
if __name__ == "__main__":
    if mode == "development":
        # bot.run(token)
        uvicorn.run(app, host="127.0.0.1", port=8000)
    elif mode == "testing":
        test()
    elif mode == "production":
        print()
