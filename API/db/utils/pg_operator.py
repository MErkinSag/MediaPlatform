import asyncpg
from typing import Any, List, Dict

from db.utils.db_operator import DBOperator


class PostgreSQLOperator(DBOperator):
    def __init__(self, config):
        self.db_user = config['contents']['username']
        self.db_user_pwd = config['contents']['password']
        self.db_name = config['contents']['database']
        self.address = config['dns_name']
        self.conn = None

    async def establish_connection(self):
        conn_string = f"postgresql://{self.db_user}:{self.db_user_pwd}@{self.address}/{self.db_name}"
        self.conn = await asyncpg.connect(conn_string)

    async def disconnect(self):
        if self.conn is not None and not self.conn.is_closed():
            await self.conn.close()
            # TODO
            # log.info("PostgreSQL connection is closed.")

    async def connected(self) -> bool:
        """
        Check whether the database connection is healthy
        :return: Whether there is a connection or not
        """
        try:
            await self.conn.fetchrow('SELECT 1')
            return True

        except asyncpg.exceptions.ConnectionDoesNotExistError:
            return False


    def format_for_sql(self, value: int | float | str) -> str:
        """
        Function to wrap the value between quotes for SQL syntax
        i.e. if val is MovieName -> formatted into 'MovieName'

        :param value: Value to be formatted
        :return: formatted value
        """
        if type(value) == str:
            return f"'{value}'"
        return str(value)



    async def insert(self, record: Dict, table: str, serial_id_column: str = None) -> int | None:
        """
        Inserts the record type of dictionary to the table (possibly with a serial id -primary key- column)
        (in case of a serial column returns the id that is generated in the database)
        :param record: the data that is going to be inserted as a dict (excluding the id attribute)
        :param table: name of the table to be inserted
        :return: The id of the inserted item or None in case of the absence of serial id column
        """



        query = f"INSERT INTO {table}({', '.join(list(record.keys()))}) " \
                f"VALUES({', '.join([self.format_for_sql(value) for value in list(record.values())])})"

        if serial_id_column is not None:
            query += f" RETURNING {serial_id_column}"

        query += ";"

        id = await self.conn.fetchval(query)

        return id

    async def select(self, table: str, where_clause: str = None) -> List[Dict]:
        """
        Retrieves records from the database as a list of dictionaries
        :param table:
        :param where_clause: conditions part of the WHERE clause for the query
        :return:
        """
        query = f"SELECT * FROM {table}"
        if where_clause is not None:
            query += f" WHERE {where_clause};"
        else:
            query += ";"
        rows = await self.conn.fetch(query)
        result_data = [{item[0]: item[1] for item in row.items()} for row in rows]
        return result_data

    async def update(self, data: Dict, match_column_values: Dict[str, Any], update_column_values: Dict[str, Any], table: str):
        update = f"{table}"
        set = ', '.join([f"{str(item1) + '=' + self.format_for_sql(item2)}" for item1, item2 in update_column_values.items()])
        where = ' AND '.join([f"{str(item1) + '=' + self.format_for_sql(item2)}" for item1, item2 in match_column_values.items()])

        query = f"UPDATE {update} SET {set} WHERE {where};"
        await self.conn.execute(query)

    async def delete(self, match_column_values: Dict[str, Any], table: str):
        where = ' AND '.join([f"{str(item1) + '=' + self.format_for_sql(item2)}" for item1, item2 in match_column_values.items()])
        query = f"DELETE FROM {table} WHERE {where};"
        await self.conn.execute(query)

