# MediaPlatform
A media platform that makes it possible for the users to upload, edit and remove media contents like movies, videos and games.

In order to build the images and run the application use 
```
docker compose up
```
which will build the images and run all of the services. The application runs on http://localhost. (if port 80 is busy can be set on docker-compose.yml ui service)

Currently there is no login page. A prompt asks for a password which is "123" for one user.

Upload parts are just for demonstration and do not upload the file content itself. They take the name of the file as the file name if none provided by the user.

Services include:

- Backend API: The layer for managing database transactions. 
- UI: The web UI layer with Streamlit
- DB: PostgreSQL
- pgAdmin: Postgre UI
