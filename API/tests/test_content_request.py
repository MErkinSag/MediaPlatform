import pytest
from fastapi.testclient import TestClient
from main import app
from contents.movie import Movie
from contents.game import Game


@pytest.fixture
def client():
    """
    A workaround for PyTest to recognize @app.on_event('startup') and
    @app.on_event('shutdown') events
    :return:
    """
    with TestClient(app) as c:
        yield c


def test_upload_movie(client):
    movie = Movie(name="Pirates of Carribean", imdb_rating=9)
    response = client.post("http://localhost:8000/contents/movies", json={"name": movie.get_name(), "imdb_rating": movie.imdb_rating})

    assert response.status_code == 200
    assert "id" in response.json()


def test_get_movies(client):
    response = client.get("http://localhost:8000/contents/movies")

    assert response.status_code == 200

    movie_list_data = response.json()

    assert type(movie_list_data) == list

    assert len(movie_list_data) > 0

    # try to build movie object with each of the results
    [Movie(**movie) for movie in movie_list_data]

def test_get_games(client):
    response = client.get("http://localhost:8000/contents/games")

    assert response.status_code == 200

    game_list_data = response.json()

    assert type(game_list_data) == list

    assert len(game_list_data) > 0

    # try to build game object with each of the results
    [Game(**game) for game in game_list_data]


def test_insert_games(client):
    game_data = {'name': 'asdsadsa', 'game_type': 'sdsdsdsd'}
    response = client.post("http://localhost:8000/contents/games", json=game_data)

    assert response.status_code == 200




def test_get_single_movie(client):
    # create a movie and send it to db
    movie = Movie(name="Pirates of Carribean", imdb_rating=9)
    response = client.post("http://localhost:8000/contents/movies", json={"name": movie.get_name(), "imdb_rating": movie.imdb_rating})

    assert response.status_code == 200

    # id was generated in the db
    movie.id = response.json()['id']

    # get the movie with the same id from the db
    response = client.get(f"http://localhost:8000/contents/movies/{movie.id}")

    assert response.status_code == 200

    retrieved_movie = Movie(**response.json())

    # assert that retrieved movie is the same with the
    assert movie == retrieved_movie


def test_update_movie(client):

    movie = Movie(name="Pirates of Carribean", imdb_rating=9)
    response = client.post("http://localhost:8000/contents/movies", json={"name": movie.get_name(), "imdb_rating": movie.imdb_rating})
    movie.id = response.json()["id"]

    # edit the name
    movie.edit_name(new_name="Pirates of Carribean 3")

    data = {"content": movie.get_attr_value_mappings(), "update_columns": ["name"]}

    response = client.put("http://localhost:8000/contents/movies", json=data)

    assert response.status_code == 200

    updated_movie_data = client.get(f"http://localhost:8000/contents/movies/{movie.id}")

    updated_movie = Movie(**updated_movie_data.json())

    assert updated_movie.id == movie.id

    assert updated_movie.get_name() == "Pirates of Carribean 3"

def test_update_game(client):
    game_data = {"content": {"id": 2, "name": "aaaa", "game_type": "Racing"}, "update_columns": ["name"]}
    response = client.put("http://localhost:8000/contents/games", json=game_data)

    pass

def test_delete_movie(client):
    # Create a movie
    movie = Movie(name="Pirates of Carribean", imdb_rating=9)
    response = client.post("http://localhost:8000/contents/movies", json={"name": movie.get_name(), "imdb_rating": movie.imdb_rating})
    movie.id = response.json()["id"]

    # Try to remove the movie
    response = client.request("DELETE", "http://localhost:8000/contents/movies", json=movie.get_attr_value_mappings())

    assert response.status_code == 200

    # Try to retrieve the item
    movie_list_data = client.get(f"http://localhost:8000/contents/movies/{movie.id}")

    assert movie.id not in [movie_data["id"] for movie_data in movie_list_data.json()]









