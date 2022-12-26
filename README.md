# MediaPlatform
A media platform that makes it possible for the users to upload, edit and remove media contents like movies, videos and games.

In order to build the images and run the application use 
```
docker compose up
```
which will build the images and run all of the services. The application runs on http://localhost. (if port 80 is busy can be set on docker-compose.yml ui service)

Currently there is no login page. A prompt asks for a password which is "123" for one user.

--> The environment variable "FILL_DB" of backend_api service in docker-compose.yml file is for creating the tables and filling them with dummy data. Simply comment it out after running the application for the first time.

Services include:

- Backend API: The layer for managing database transactions. 
- UI: The web UI layer with Streamlit
- DB: PostgreSQL
- pgAdmin: Postgre UI
