# IAQ Frontend

## Prerequisites
To run this app, please install [Node](https://nodejs.org/en) if it isn't already installed.
After that, you will need to perform a `npm install` in the root directory of `frontend`.


## Setting up and Testing Frontend
To get the frontend to work with your installation of the backend, you need to head into `src/lib/logic/host.js`.

This file will include details on the Flask host (the backend) and you may only need to edit the values for `flaskHost` and `flaskPort`.

You can test if the frontend is working with the backend by running `npm run dev -- --host` and head to `http://[ip_address]:5173`. If you can see that the frontend is fetching data from the backend. You may now move on to the building section.

## Building
To prepare the frontend for use in a "production" state, you will need to run `npm run build`. This will build a "production" version of the svelte project ready for deployment.

You can test if the build was successful by running `npm run preview -- --host --port=5173` and heading to `http://[ip_address]:5173`. If it seems to be fetching data from the backend, this means the frontend build is successful.

## Additional Notes
If you want to setup the Frontend to start on boot of the Raspberry Pi, head to the `services` directory and read the `README.md`