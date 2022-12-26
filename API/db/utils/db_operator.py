from abc import ABC, abstractmethod


class DBOperator(ABC):
    @abstractmethod
    async def establish_connection(self, *args, **kwargs):
        pass

    @abstractmethod
    async def disconnect(self):
        pass

    @abstractmethod
    async def connected(self) -> bool:
        """
        Method to test the database connection is still alive
        :return:
        """
        pass

    @abstractmethod
    async def insert(self, *args, **kwargs):
        pass

    @abstractmethod
    async def select(self, *args, **kwargs):
        pass

    @abstractmethod
    async def update(self, *args, **kwargs):
        pass

    @abstractmethod
    async def delete(self, *args, **kwargs):
        pass
