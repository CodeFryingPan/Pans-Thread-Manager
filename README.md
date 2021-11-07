# Pans-News-Feed-Bot

## Setup 

This is a step by step guide to setup the Pan's News Feed Bot for Pan's Kitchen

### Requirements


Python 3.6.1+, Pip 

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

### Running FastAPI


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

### Running Tests


##### All Tests

Set the `value` of FAST_API_CONFIG to `testing` and run:

```
python3 manage.py
```

Or using a debugger in Pycharm or VSCode.


##### Specific Tests

```
python3 -m unittest discover tests/<directory>
```

`<directory>` can be either `api`, `integrations`, or `unit`.


##### Specific Files:


```
python3 -m unittest tests/<directory>/test_*.py
```

`<directory>` can be either `api`, `integrations`, or `unit`. 
`*` is the name of the file after test.

##### Notes:

All tests must be named `test_*.py` to be detected by unittest. 

Base tests (that are not meant to be run) should be named `base_*_test.py`.

## How to help the creation of the bot?

[Guide on how to commit for Pan's News Feed Bot](COMMIT.md)

## License

[License](LICENSE)
