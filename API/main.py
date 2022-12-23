from fastapi import FastAPI

app = FastAPI()


@app.get("/data")
def get_data():
    return {"movies": {"movie1": {"name": "movie_one","review": 1}, "movie2": {"name": "movie_two", "review": 5}}}


