from contents.media_content import MediaContent


class Game(MediaContent):
    def __init__(self, name: str, game_type: str, id: int = None):
        super().__init__(name, id)
        self.game_type = game_type

