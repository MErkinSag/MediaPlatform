from db.media.PostgreMediaDB import PostgreMediaDB
from config.utils import Config
from contents.movie import Movie
import pytest


@pytest.mark.asyncio
async def test_connection():
    # TODO get the config
    config = Config("config.yml")
    pg_media_db = PostgreMediaDB(config)
    await pg_media_db.connect()

    assert await pg_media_db.is_connection_alive()

    await pg_media_db.disconnect()

@pytest.mark.asyncio
async def test_insert_movie_record():
    config = Config("config.yml")
    pg_media_db = PostgreMediaDB(config)
    await pg_media_db.connect()

    test_movie = Movie(name="Fight Club", imdb_rating=9.2)

    await pg_media_db.insert_content(test_movie)

    # the id was actually generated in the database
    assert type(test_movie.id) == int

    # retrieve the records and check whether the new content is there
    movies = await pg_media_db.get_movie_contents()
    found = False
    for movie in movies:
        if movie.id == test_movie.id:
            found = True
            break

    assert found

    # remove the test content
    await pg_media_db.remove_media_content(test_movie)

    await pg_media_db.disconnect()


@pytest.mark.asyncio
async def test_retrieve_movie_records():
    config = Config("config.yml")

    pg_media_db = PostgreMediaDB(config)

    await pg_media_db.connect()

    movies = await pg_media_db.get_movie_contents()

    await pg_media_db.disconnect()

    assert [type(movie) == Movie for movie in movies]


@pytest.mark.asyncio
async def test_update_movie_record():
    """
    1. Retrieve the first movie in the database
    2. Update the name of the movie object
    3. Send the updated object to the database
    4. Retrieve the updated object back from database
    5. Validate the name is updated
    6. Update the name to the old one again
    :return:
    """
    config = Config("config.yml")

    pg_media_db = PostgreMediaDB(config)

    await pg_media_db.connect()

    movies = await pg_media_db.get_movie_contents()

    test_movie = movies[0]

    test_movie_id = test_movie.id

    test_movie_oldname = test_movie.get_name()

    test_movie.edit_name(new_name="Toy Story")

    await pg_media_db.update_media_content(test_movie, ["name"])

    # Retrieve the updated object back from the resulting objects
    test_movie_updated = await pg_media_db.get_movie_contents(id=test_movie_id)

    assert test_movie_updated.get_name() == "Toy Story"

    # Update back the movie name in database
    test_movie.edit_name(new_name=test_movie_oldname)
    await pg_media_db.update_media_content(test_movie, ["name"])

    await pg_media_db.disconnect()

@pytest.mark.asyncio
async def test_delete_movie_record():
    config = Config("config.yml")

    pg_media_db = PostgreMediaDB(config)

    await pg_media_db.connect()

    movies = await pg_media_db.get_movie_contents()

    test_movie = movies[0]

    test_movie_id = test_movie.id

    await pg_media_db.remove_media_content(test_movie)

    movies = await pg_media_db.get_movie_contents()

    test_movie_found = False
    for movie in movies:
        if movie.id == test_movie_id:
            test_movie_found = True
            break

    assert not test_movie_found

    # insert back test movie to the database (it will be a different id)
    await pg_media_db.insert_content(test_movie)

    await pg_media_db.disconnect()
