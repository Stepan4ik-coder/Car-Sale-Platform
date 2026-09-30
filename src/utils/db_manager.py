from src.repos.cars import CarsRepository
from src.repos.chats import ChatsRepository
from src.repos.favorites import FavoritesRepository
from src.repos.messages import MessagesRepository
from src.repos.user import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.cars = CarsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.favorites = FavoritesRepository(self.session)
        self.chats = ChatsRepository(self.session)
        self.messages = MessagesRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
