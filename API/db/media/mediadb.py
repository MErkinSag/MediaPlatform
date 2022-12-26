from abc import ABC, abstractmethod
from db.utils.db_operator import DBOperator
from contents.media_content import MediaContent


class MediaDB(ABC):
    """
    Database abstraction for any database for a media content
    """

    def __init__(self, config, db_operator: DBOperator):
        self.config = config
        self.db_operator = db_operator

    async def connect(self):
        try:
            await self.db_operator.establish_connection()
        except Exception as e:
            raise ConnectionError(f"Could not connect to the database for media contents: {str(e)}")

    async def disconnect(self):
        await self.db_operator.disconnect()
