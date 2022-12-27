import os
import asyncio
from fastapi import FastAPI
from db.media.PostgreMediaDB import PostgreMediaDB
from config.utils import Config
from models import MovieContent, VideoContent, GameContent, UpdateVideoContent, UpdateMovieContent, UpdateGameContent, create_movie, create_game, create_video
import uvicorn

app = FastAPI()
config = Config("config.yml")

media_db = PostgreMediaDB(config)


@app.get("/")
def healthcheck():
    return {"msg": "server is up and running"}


@app.get("/mock_movie_data")
def get_data():
    return {"movies": {"movie1": {"name": "movie_one", "review": 1}, "movie2": {"name": "movie_two", "review": 5}}}


@app.get("/contents/movies")
async def get_all_movies():
    movie_list = await media_db.get_movie_contents()

    movie_list_data = [movie.get_attr_value_mappings() for movie in movie_list]

    return movie_list_data



@app.get("/contents/videos")
async def get_all_videos():
    video_list = await media_db.get_video_contents()

    video_list_data = [video.get_attr_value_mappings() for video in video_list]

    return video_list_data


@app.get("/contents/games")
async def get_all_games():
    game_list = await media_db.get_game_contents()

    game_list_data = [game.get_attr_value_mappings() for game in game_list]

    return game_list_data


@app.get("/contents/movies/{id}")
async def get_movie(id: int):
    movie = await media_db.get_movie_contents(id=id)

    if movie == []:
        return movie

    movie_data = movie.get_attr_value_mappings()

    return movie_data


@app.get("/contents/videos/{id}")
async def get_video(id: int):
    video = await media_db.get_video_contents(id=id)

    if video == []:
        return video

    video_data = video.get_attr_value_mappings()

    return video_data


@app.get("/contents/games/{id}")
async def get_game(id: int):
    game = await media_db.get_game_contents(id=id)

    if game == []:
        return game

    game_data = game.get_attr_value_mappings()

    return game_data


@app.post("/contents/movies")
async def insert_movie(movie_content: MovieContent):
    movie = create_movie(movie_content)
    await media_db.insert_content(movie)

    return {"id": movie.id}


@app.post("/contents/videos")
async def insert_video(video_content: VideoContent):
    video = create_video(video_content)
    await media_db.insert_content(video)
    return {"id": video.id}


@app.post("/contents/games")
async def insert_game(game_content: GameContent):
    game = create_game(game_content)
    await media_db.insert_content(game)
    return {"id": game.id}


@app.put("/contents/movies")
async def update_movie(update_movie: UpdateMovieContent):
    movie = create_movie(update_movie.content)
    await media_db.update_media_content(movie, update_movie.update_columns)


@app.put("/contents/videos")
async def update_video(update_video: UpdateVideoContent):
    video = create_video(update_video.content)
    await media_db.update_media_content(video, update_video.update_columns)


@app.put("/contents/games")
async def update_game(update_game: UpdateGameContent):
    game = create_game(update_game.content)
    await media_db.update_media_content(game, update_game.update_columns)


@app.delete("/contents/movies")
async def remove_movie(movie_content: MovieContent):
    movie = create_movie(movie_content)
    await media_db.remove_media_content(movie)


@app.delete("/contents/videos")
async def remove_video(video_content: VideoContent):
    video = create_video(video_content)
    await media_db.remove_media_content(video)


@app.delete("/contents/games")
async def remove_game(game_content: GameContent):
    game = create_game(game_content)
    await media_db.remove_media_content(game)


@app.on_event("startup")
async def startup():
    await media_db.connect()


@app.on_event("shutdown")
async def shutdown():
    await media_db.disconnect()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
