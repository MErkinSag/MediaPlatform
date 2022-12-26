from contents.media_content import MediaContent


class Video(MediaContent):
    def __init__(self, name: str, year: int, id: int = None):
        super().__init__(name, id)
        self.year = year

