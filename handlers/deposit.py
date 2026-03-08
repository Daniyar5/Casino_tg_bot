from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from forms.user import DepositForm
from database import get_db_connection
from keyboards import get_cancel_keyboard, get_main_reply_keyboard

router = Router()

@router.message(Command('cancel'))
@router.message(F.text.lower() == 'отмена')
async def cancel_form(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('❌Отмена сделана!❌', reply_markup=get_main_reply_keyboard())

@router.message(Command('dep'))
@router.message(F.text.lower() == 'депозит')
async def deposit(message: Message, state: FSMContext):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        await message.answer('Как ты собрался депать не зарегавшись?Сначала зарегистрируйся с помощью /start.', reply_markup=get_main_reply_keyboard())
        return

    await message.answer('Введи номер карты (16 цифр, скам):', reply_markup=get_cancel_keyboard())
    await state.set_state(DepositForm.card_number)

@router.message(DepositForm.card_number, F.text)
async def process_card_number(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await cancel_form(message, state)
        return

    card_number = message.text
    if not card_number.isdigit() or len(card_number) != 16:
        await message.answer('Номер карты должен быть 16 цифр.', reply_markup=get_cancel_keyboard())
        return

    await state.update_data(card_number=card_number)
    await message.answer('Введи дату истечения (MM/YY):', reply_markup=get_cancel_keyboard())
    await state.set_state(DepositForm.expiry)

@router.message(DepositForm.expiry, F.text)
async def process_expiry(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await cancel_form(message, state)
        return

    expiry = message.text
    if not (len(expiry) == 5 and expiry[2] == '/' and expiry[:2].isdigit() and expiry[3:].isdigit()):
        await message.answer('Формат: MM/YY.', reply_markup=get_cancel_keyboard())
        return

    await state.update_data(expiry=expiry)
    await message.answer('Введи 3 цифры с другой стороны карты CVV (3 цифры):', reply_markup=get_cancel_keyboard())
    await state.set_state(DepositForm.cvv)

@router.message(DepositForm.cvv, F.text)
async def process_cvv(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await cancel_form(message, state)
        return

    cvv = message.text
    if not cvv.isdigit() or len(cvv) != 3:
        await message.answer('CVV должен быть 3 цифры.', reply_markup=get_cancel_keyboard())
        return

    await state.update_data(cvv=cvv)
    await message.answer('Введи сумму пополнения (число):', reply_markup=get_cancel_keyboard())
    await state.set_state(DepositForm.amount)

@router.message(DepositForm.amount, F.text)
async def process_amount(message: Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await cancel_form(message, state)
        return

    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer('Сумма должна быть положительным числом.', reply_markup=get_cancel_keyboard())
        return

    amount = int(message.text)
    user_id = message.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    cursor.execute('INSERT INTO transactions (user_id, amount) VALUES (?, ?)', (user_id, amount))
    conn.commit()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    new_balance = cursor.fetchone()['balance']
    conn.close()

    await message.answer(f'Счет пополнен на {amount}. Новый баланс: {new_balance}', reply_markup=get_main_reply_keyboard())
    await state.clear()

    video = FSInputFile("videos/money.mp4")
    await message.answer_video(video)