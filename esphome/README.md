# IAQ ESPHOME

## Prerequisites
### !! You may need to run this on a seperate device !!

To run this app, please ensure [Python 3](https://www.python.org/) is installed on the Raspbery Pi if it isn't already installed.

After that, ensure you are in the root directory of `esphome` and create and activate the Python Virtual Environment with:
```
python3 -m venv .venv
. .venv/bin/activate
```

Once the the environment has been created, run the command:
```
pip install -r requirements.txt
```
This should install all the dependencies needed for running the esphome.

## Running ESPHome
Once all dependencies have been installed, running the backend should be as simple as running:
```
esphome dashboard config
```
Ensure that the environment is activated or else it won't run with the installed dependencies.

You can access esphome by heading to `http://localhost:6052`. It should show you the ESPHome Web Dashboard.