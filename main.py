import asyncio
from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database import init_db

from handlers.common import router as common_router
from handlers.registration import router as registration_router
from handlers.deposit import router as deposit_router
from handlers.balance import router as balance_router
from handlers.history import router as history_router
from handlers.game import router as game_router

load_dotenv()
TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher(storage=MemoryStorage()) 

dp.include_router(registration_router)  
dp.include_router(deposit_router)
dp.include_router(balance_router)
dp.include_router(history_router)
dp.include_router(game_router)
dp.include_router(common_router)  

async def main():
    init_db()
    bot = Bot(token=TOKEN)
    print('Start...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())