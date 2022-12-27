#!/bin/sh


# source: https://pranavmalvawala.com/run-script-only-on-first-start-up

# This script checks if the container is started for the first time.

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP
    # place your script that you only want to run on first startup.
    python -m db.dummy.fill_db && uvicorn main:app --host 0.0.0.0 --port 8000

else
    # script that should run the rest of the times (instances where you 
    # stop/restart containers).
    uvicorn main:app --host 0.0.0.0 --port 8000
fi
