from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from forms.user import UserForm
from database import get_db_connection
from keyboards import get_main_reply_keyboard

router = Router()

@router.message(Command("start"))
@router.message(F.text.lower() == 'старт')
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        await message.answer('Ты уже зарегистрирован. Добро пожаловать обратно!', reply_markup=get_main_reply_keyboard())
    else:
        await message.answer('Бедолага, сначала надо зарегистрироваться.\nДля начала пиши своё имя:', reply_markup=ReplyKeyboardRemove())
        await state.set_state(UserForm.name)

@router.message(UserForm.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Молодец.\nА теперь давай пиши свой возраст:')
    await state.set_state(UserForm.age)

@router.message(UserForm.age, F.text)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Ты считать не умеешь? Бро, пиши число.')
        return

    age = int(message.text)
    if age < 18:
        await message.answer('Мелковат ты. Сюда можно только с 18.')
        return
    elif age > 100:
        await message.answer('Староват ты. Пошел вон отсюда. Сюда только молоденьким меньше 100 лет можно.')
        return

    await state.update_data(age=age)
    await message.answer('Окей.\nГони сюда свой email:')
    await state.set_state(UserForm.email)

@router.message(UserForm.email, F.text)
async def process_email(message: Message, state: FSMContext):
    email_text = message.text
    if '@' not in email_text or '.' not in email_text:
        await message.answer('Ступид персон. Надо нормально email писать.')
        return

    await state.update_data(email=email_text)
    data = await state.get_data()
    name = data['name']
    age = data['age']
    email = data['email']
    user_id = message.from_user.id

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, name, age, email, balance)
        VALUES (?, ?, ?, ?, 0)
    ''', (user_id, name, age, email))
    conn.commit()
    conn.close()

    await message.answer(f'Поздравляю, теперь у меня есть инфа о тебе.\nИмя: {name}\nВозраст: {age}\nПочта: {email}')
    await state.clear()
    await message.answer('Теперь можешь пользоваться ботом!', reply_markup=get_main_reply_keyboard())