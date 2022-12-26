from typing import List
from contents.video import Video
from contents.movie import Movie
from contents.game import Game

from pydantic import BaseModel

class MovieContent(BaseModel):
    id: int | None
    name: str
    imdb_rating: float

class VideoContent(BaseModel):
    id: int | None
    name: str
    year: int

class GameContent(BaseModel):
    id: int | None
    name: str
    game_type: str

class UpdateVideoContent(BaseModel):
    content: VideoContent
    update_columns: List[str]

class UpdateMovieContent(BaseModel):
    content: MovieContent
    update_columns: List[str]

class UpdateGameContent(BaseModel):
    content: GameContent
    update_columns: List[str]


def create_movie(movie_data: MovieContent) -> Movie:
    return Movie(id=movie_data.id, name=movie_data.name, imdb_rating=movie_data.imdb_rating)

def create_video(video_data: VideoContent) -> Video:
    return Video(id=video_data.id, name=video_data.name, year=video_data.year)

def create_game(game_data: GameContent) -> Game:
    return Game(id=game_data.id, name=game_data.name, game_type=game_data.game_type)
