#!/bin/sh


# source: https://pranavmalvawala.com/run-script-only-on-first-start-up

# This script checks if the container is started for the first time.

CONTAINER_FIRST_STARTUP="CONTAINER_FIRST_STARTUP"

# IF THIS IS THE FIRST STARTUP OF THE CONTAINER (i.e. The file was not created yet with the first docker run or docker compose up)
if [ ! -e /$CONTAINER_FIRST_STARTUP ]; then
    touch /$CONTAINER_FIRST_STARTUP

    # create the tables on the database and fill them with dummy data, then start the fast api with uvicorn async worker
    python -m db.dummy.fill_db && uvicorn main:app --host 0.0.0.0 --port 8000

else
    # just start the fast api with uvicorn async worker
    uvicorn main:app --host 0.0.0.0 --port 8000
fi
