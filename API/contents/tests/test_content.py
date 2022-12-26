from movie import Movie

def test_movie():
    movie = Movie(name="Fight Club", imdb_rating=9.1)
    print(movie.get_attr_value_mappings())
    assert movie.get_content_type() == "movie"
    assert movie.get_attr_value_mappings() == {'id': None, 'name': 'Fight Club', 'imdb_rating': 9.1}
