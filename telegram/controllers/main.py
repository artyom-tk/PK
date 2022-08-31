from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Database
from databases.sqlite.sqlite import Sqlite

# Controllers
from .start import StartController
from .unknown import UnknownController

# Middlewares
from ..middlewares.activity import ActivityMiddleware


class MainController:
    controllers = {}
    middlewares = {}

    def __init__(self, token):
        self.__bot = Bot(token=token)
        self.__dispatcher = Dispatcher(self.__bot, storage=MemoryStorage())
        self.__database = Sqlite()

        # Set controllers
        self.set_controllers(StartController, UnknownController)

        # Set middlewares
        self.set_middlewares(ActivityMiddleware)

        print(f'Active controllers: {self.controllers}')
        print(f'Active middlewares: {self.middlewares}')

        executor.start_polling(self.__dispatcher, skip_updates=True)

    def set_controllers(self, *controllers):
        for controller in controllers:
            self.controllers[controller.__name__] = controller(self.__bot, self.__dispatcher, self.__database)

    def set_middlewares(self, *middlewares):
        for middleware in middlewares:
            self.middlewares[middleware.__name__] = middleware(self.__database)
