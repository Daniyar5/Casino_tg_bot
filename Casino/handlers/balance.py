from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from database import get_db_connection

router = Router()

@router.message(Command('balance'))
@router.message(F.text.lower() == 'баланс')
async def balance(message: Message):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        await message.answer('Перед депанием нужно обязательно зарегаться, сначала зарегистрируйся с помощью /start.')
        return

    await message.answer(f'Твой баланс: {user["balance"]}')