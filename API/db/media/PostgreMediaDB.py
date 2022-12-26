from db.media.mediadb import MediaDB
from contents.media_content import MediaContent
from db.utils.pg_operator import PostgreSQLOperator
from typing import List, Dict, Any
from contents.movie import Movie
from contents.video import Video
from contents.game import Game


class PostgreMediaDB(MediaDB):
    """
    PostgreSQL related operations on Media Content objects
    """
    def __init__(self, config, postgre_operator: PostgreSQLOperator=None):

        # take the postgres related part from the config
        pg_config = config()['db']['pg']

        if not postgre_operator:    # if the operator was given with the constructor
            postgre_operator = PostgreSQLOperator(pg_config)  # create the operator

        super().__init__(pg_config, postgre_operator)

        self.content_db = self.config['contents']['database']
        self.table_mapping = self.config['contents']['tables']

    def _get_content_db_table(self, content: MediaContent):
        """
        Get the name of the table for the corresponding content
        :param content: A content, e.g. video
        :return: name of the table
        """
        content_type = content.get_content_type()  # content_type can be "movie", "video" or "game"

        return self.table_mapping[content_type]

    async def insert_content(self, content: MediaContent):
        content_as_dict = content.get_attr_value_mappings()

        # remove the id since it is None as the object is not in the db yet
        del content_as_dict["id"]

        table = self._get_content_db_table(content)

        id = await self.db_operator.insert(record=content_as_dict, table=table, serial_id_column="id")

        content.id = id

    async def update_media_content(self, content: MediaContent, update_columns: List[str]):

        if "id" in update_columns:
            raise Exception("Cannot update ID column.")

        table = self._get_content_db_table(content)
        data = content.get_attr_value_mappings()
        match_column_values = {"id": content.id}
        update_columns = {key:value for key, value in data.items() if key in update_columns}
        await self.db_operator.update(data=data, match_column_values=match_column_values,update_column_values=update_columns, table=table)

    async def remove_media_content(self, content: MediaContent):
        table = self._get_content_db_table(content)
        match_column_values = content.get_attr_value_mappings()
        await self.db_operator.delete(match_column_values=match_column_values, table=table)

    async def get_movie_contents(self, id: int | None = None) -> Movie | List[Movie]:
        table = self.table_mapping["movie"]

        condition = None

        if id is not None:
            condition = f"id={id}"

        movies_data = await self.db_operator.select(table, where_clause=condition)

        result = [Movie(**data) for data in movies_data]

        # if an id was specified on the function call
        if id is not None:
            # if there the query result is not empty
            # (preventing List index out of range exception)
            if len(result):
                return result[0]
        return result

    async def get_video_contents(self, id: int | None = None) -> Video | List[Video]:
        table = self.table_mapping["video"]

        condition = None

        if id is not None:
            condition = f"id={id}"

        videos_data = await self.db_operator.select(table, where_clause=condition)
        result = [Video(**data) for data in videos_data]
        if id is not None:
            return result[0]
        return [Video(**data) for data in videos_data]

    async def get_game_contents(self, id: int | None = None) -> Game | List[Game]:
        table = self.table_mapping["game"]

        condition = None

        if id is not None:
            condition = f"id={id}"

        games_data = await self.db_operator.select(table, where_clause=condition)

        result = [Game(**data) for data in games_data]

        if id is not None:
            return result[0]
        return result

    async def is_connection_alive(self):
        return await self.db_operator.connected()
