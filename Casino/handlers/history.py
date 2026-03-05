from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime

from database import get_db_connection

router = Router()

@router.message(Command('history'))
@router.message(F.text.lower() == 'история')
async def history(message: Message):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        await message.answer('Сначала зарегистрируйся с помощью /start.')
        conn.close()
        return

    cursor.execute('''
        SELECT amount, timestamp FROM transactions 
        WHERE user_id = ? ORDER BY timestamp DESC LIMIT 5
    ''', (user_id,))
    transactions = cursor.fetchall()
    conn.close()

    if not transactions:
        await message.answer('У тебя пока нет транзакций.')
        return

    response = 'Твоя история пополнений (последние 5):\n'
    for tx in transactions:
        formatted_time = datetime.strptime(tx['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')
        response += f'Сумма: {tx["amount"]}, Дата: {formatted_time}\n'

    await message.answer(response)