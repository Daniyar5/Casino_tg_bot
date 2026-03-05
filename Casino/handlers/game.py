import random
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from database import get_db_connection
from aiogram.fsm.state import State, StatesGroup

router = Router()

class GameState(StatesGroup):
    waiting_bet = State()


@router.message(Command('play'))
@router.message(F.text == "Играть")
async def start_game(message: Message, state: FSMContext):
    await message.answer("Напиши сумму ставки:")
    await state.set_state(GameState.waiting_bet)


@router.message(GameState.waiting_bet)
async def play_game(message: Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Введите число")
        return

    bet = int(message.text)

    user_id = message.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE user_id = ?", (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        await message.answer("Ты не зарегистрирован")
        return

    balance = user["balance"]

    if bet > balance:
        await message.answer("Недостаточно бабок на балансе")
        return


    win = random.choice([True, False])

    if win:

        new_balance = balance + bet

        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, user_id)
        )

        conn.commit()

        video = FSInputFile("videos/luck-777.mp4")

        await message.answer_video(
            video,
            caption=f"🎉 Ты поднял бабки!\nВыигрыш: {bet*2}\nБаланс: {new_balance}"
        )
        
        await state.clear()

    else:

        new_balance = balance - bet

        cursor.execute(
            "UPDATE users SET balance = ? WHERE user_id = ?",
            (new_balance, user_id)
        )

        conn.commit()

        video = FSInputFile("videos/unluck.mp4")

        await message.answer_video(
            video,
            caption=f"💀 Ты просрал бабки\nПотеряно: {bet}\nБаланс: {new_balance}"
        )

        await state.clear()