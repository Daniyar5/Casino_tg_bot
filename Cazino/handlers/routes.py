from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
                           )
from forms.user import Form
from aiogram.fsm.context import FSMContext

router = Router()


def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text='Старт')],
        [KeyboardButton(text='Депнуть'), KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True
    )

    return keyboard

def get_main_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Открыть сайт', url='https://google.com')],
            [InlineKeyboardButton(text='Подробнее', callback_data='info_more')]

        ],
    )

    return keyboard


@router.callback_query(lambda c: c.data == 'info_more')
async def proccess_more_info(callback: CallbackQuery):
    await callback.message.answer('Ты гей')
    await callback.answer()


@router.message(Command("start"))
@router.message(F.text.lower() == 'старт')
async def start(massege: Message, state: FSMContext):
    await massege.answer('Бедолага, с начало надо зарегатся.\nДля начало пиши своё имя:')
    await state.set_state(Form.name)


@router.message(Command('cancel'))
async def cancel_from(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Отмен сделал!')


@router.message(Form.name, F.text)
async def proccess_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer('Молодец.\nА теперь давай пиши свой возраст:')
    await state.set_state(Form.age)


@router.message(Form.age, F.text)
async def proccess_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Ты считать не умеешь? Брооо пиши число.')
        return
    
    if int(message.text) < 18:
        await message.answer('Мелковат ты. Сюда можно толко с 18')
        return
    elif int(message.text) > 100:
        await message.answer('Староват ты. Пощёл вон от сюда. Сюда только молоденьким меншье 100 лет можно.')
        return

    await state.update_data(age=int(message.text))

    await message.answer('Староват ты.\nГони сюда свой email:')
    await state.set_state(Form.email)


@router.message(Form.email, F.text)
async def proccess_email(message: Message, state: FSMContext):
    email_text = message.text
    if '@' not in email_text or '.' not in email_text:
        await message.answer('Ступид персон. Надо нормально emeil писать.')
        return

    await state.update_data(email=email_text)

    data = await state.get_data()
    name = data['name']
    age = data['age']
    email = data['email']

    await message.answer(f'Поздравяю, теперь у меня есть инфа на тебя.\nИмя: {name}\nВозраст: {age}\nПочта: {email}')
    await state.clear()







@router.message(Command('help'))
@router.message(F.text.lower() == 'помощь')
async def help(massege: Message):
    await massege.answer('Команды:\n/start - запустить бота\n/help - список команд\n/about - про нас')

@router.message(Command('about'))
async def about(massege: Message):
    await massege.answer(
        f'Это ультра мега казик для <a href="https://img.itch.zone/aW1nLzE0NDgyNTc5LmpwZw==/original/h6BwgP.jpg">настоящих мужиков</a>.\nЯ знаю кто ты: {massege.from_user.first_name}',
        parse_mode='HTML',
        reply_markup=get_main_inline_keyboard()
        )
        
    
@router.message()
async def чё(massege: Message):
    await massege.answer('Чё?')