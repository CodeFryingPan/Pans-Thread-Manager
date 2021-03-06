# Pans Thread Manager

## Setup 

This is a step by step guide to setup the Pan's News Feed Bot for Pan's Kitchen

### Requirements


Python 3.9,7+, Pip 

### Virtual Environment

Start up your Terminal (Unix) or Powershell, and `cd` into the Project directory root folder.

Create a virtual environment for this project using `venv` in Python 3:

```zsh
python3 -m venv env
```
Note: The environment name "env" can be changed to whatever you want. Just make sure to not add it in your commits.

Start the virtual environment using:
```zsh
source env/bin/activate
```

To close the environment use `deactivate`



The list of all the necessary dependencies can be found in the requirements.txt. 
To install all of the necessary dependencies in it use:

```text
pip install -r path/to/requirements.txt
```

When finished check your dependencies with:

```text
pip list
```

### Running FastAPI with Discord.py 

This will be used specifically to be able to use the Discord Bot via HTTPS Requests in the future (either on an external app or form).

To run FastAPI locally either run the server using uvicorn (ASGI Server) on your terminal with:
```
uvicorn manage:app --reload
```

Or using:

```text
python3 manage.py
```

Or using a debugger in Pycharm or VSCode

To change the runtime mode, create a file named `.env`:
```text
FAST_API_CONFIG=value
```
`value` can be either `development`, `production`, `testing`. If not defined it will fallback to `development`.


Once ran, check `http://127.0.0.1:8000`.


Congrats you got FastAPI is running locally and you're all set to develop in the backend now!

### Running The bot

Simply use python3 run.py an this should work:

```text
python3 run.py
```

### Running Tests


##### All Tests

Set the `value` of FAST_API_CONFIG to `testing` and run:

```zsh
python3 manage.py
```

Or using a debugger in Pycharm or VSCode.


##### Specific Tests

```zsh
python3 -m unittest discover tests/<directory>
```

`<directory>` can be either `api`, `integrations`, or `unit`.


##### Specific Files:


```zsh
python3 -m unittest tests/<directory>/test_*.py
```

`<directory>` can be either `api`, `integrations`, or `unit`. 
`*` is the name of the file after test.

##### Notes:

All tests must be named `test_*.py` to be detected by unittest. 

Base tests (that are not meant to be run) should be named `base_*_test.py`.

## CONFIG REQUIREMENTS

Create a .env file and channels.json file for the purpose of reading date:


Channels.json example:
```json
{
    "channels" : [
        {
            "id": <CHANNEL_ID>,
            "emojis": [ <EMOJI_ID>],
            "role_to_give": <ROLE_ID>,
            "template": "--------\n\n            **TITLE** (Atleast 10 characters long + CTRL+B or COMMAND+B)\n\n                                    CONTENT (Alteast 30 characters long)\n\n            --------",
            "embed": false,
            "footer": "How to bold title in markdown: **title**",
            "validator": {
                "minimum_lines": 3,
                "title_bold": true,
                "title_length": 10,
                "description_length": 30
            }
        },
    ]   
}


```


.env should look like this:
```zsh
FAST_API_CONFIG=development
DISCORD_TOKEN=<BOT_TOKEN>

```

## How to help the creation of the bot?

[Guide on how to commit for Pan's News Feed Bot](COMMIT.md)

## License

[License](LICENSE)





