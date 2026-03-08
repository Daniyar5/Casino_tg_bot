from aiogram import Router, F
from aiogram.filters import Command, StateFilter  
from aiogram.types import Message, CallbackQuery

from keyboards import get_main_inline_keyboard

router = Router()

@router.callback_query(lambda c: c.data == 'info_more')
async def process_more_info(callback: CallbackQuery):
    await callback.message.answer('Ты гей')
    await callback.answer()

@router.message(Command('help'))
@router.message(F.text.lower() == 'помощь')
async def help_command(message: Message):
    await message.answer('Команды:\n/start - запустить бота\n/dep - пополнить счет\n/balance - проверить баланс\n/play - играть в рулетку\n/history - история\n/help - список команд\n/about - про нас')

@router.message(Command('about'))
async def about(message: Message):
    await message.answer(
        'Это ультра мега казик для <a href="https://img.itch.zone/aW1nLzE0NDgyNTc5LmpwZw==/original/h6BwgP.jpg">настоящих мужиков</a>.',
        parse_mode='HTML',
        reply_markup=get_main_inline_keyboard()
    )

@router.message(StateFilter(None)) 
async def unknown(message: Message):
    await message.answer('Чё?')