# IAQ Backend

## Prerequisites
To run this app, please ensure [Python 3](https://www.python.org/) is installed on the Raspbery Pi if it isn't already installed.

After that, ensure you are in the root directory of `backend` and create and activate the Python Virtual Environment with:
```
python3 -m venv .venv
. .venv/bin/activate
```

Once the the environment has been created, run the command:
```
pip install -r requirements.txt
```
This should install all the dependencies needed for running the backend.

## Running and Testing Backend
Once all dependencies have been installed, running the backend should be as simple as running:
```
python app.py
```
Ensure that the environment is activated or else it won't run with the installed dependencies.

You can test if the backend is running by heading to `http://[ip_address]:5500`. It should say "Flask server is running".

## Additional Notes
If you want to setup the Backend to start on boot of the Raspberry Pi, head to the `services` directory and read the `README.md`