import asyncpg
import asyncio
from config.utils import Config


async def create_dummy_video_table(conn):
    await conn.execute('''
    CREATE TABLE videos(
        id serial PRIMARY KEY,
        name text,
        year smallint
    )
    ''')


async def create_dummy_movie_table(conn):
    await conn.execute('''
    CREATE TABLE movies(
        id serial PRIMARY KEY,
        name text,
        imdb_rating double precision
    )
    ''')


async def create_dummy_game_table(conn):
    await conn.execute('''
    CREATE TABLE games(
        id serial PRIMARY KEY,
        name text,
        game_type text
    )
    ''')


async def fill_dummy_movie_table(conn):
    res = await conn.fetchval('''
    INSERT INTO movies(name, imdb_rating) VALUES ('Fight Club', 9.2), ('Toy Story', 8.2);
    ''')


async def fill_dummy_game_table(conn):
    res = await conn.fetchval('''
    INSERT INTO games(name, game_type) VALUES ('Bioshock', 'Adventure'), ('NFS', 'Racing');
    ''')
    print(f"ID: {res}, type:{type(res)}")


async def fill_dummy_video_table(conn):
    res = await conn.fetchval('''
    INSERT INTO videos(name, year) VALUES ('Summer-Vacation.mp4', 2017), ('Wedding.mp4', 2010);
    ''')


async def fill_db_with_dummy_data(config):
    config = config()['db']['pg']
    db_user = config['contents']['username']
    db_user_pwd = config['contents']['password']
    db_name = config['contents']['database']
    address = config['dns_name']

    conn_string = f"postgresql://{db_user}:{db_user_pwd}@{address}/{db_name}"
    conn = await asyncpg.connect(conn_string)

    await create_dummy_movie_table(conn)
    print(f"Table movies created")
    await create_dummy_video_table(conn)
    print(f"Table videos created")
    await create_dummy_game_table(conn)
    print(f"Table games created")
    await fill_dummy_movie_table(conn)
    print(f"Table movies is filled with dummy data")
    await fill_dummy_video_table(conn)
    print(f"Table videos is filled with dummy data")
    await fill_dummy_game_table(conn)
    print(f"Table games is filled with dummy data")
    await conn.close()


if __name__ == "__main__":
    config = Config("config.yml")
    asyncio.run(fill_db_with_dummy_data(config))
