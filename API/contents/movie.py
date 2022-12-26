from contents.media_content import MediaContent


class Movie(MediaContent):
    def __init__(self, name: str, imdb_rating: float, id: int = None):
        super().__init__(name, id)
        self.imdb_rating = imdb_rating

