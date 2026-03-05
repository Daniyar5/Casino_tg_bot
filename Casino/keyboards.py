from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
)

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Старт')],
            [KeyboardButton(text='Депозит'), KeyboardButton(text='Баланс'), KeyboardButton(text='История')],
            [KeyboardButton(text='Играть')],   # новая кнопка
            [KeyboardButton(text='Помощь')]
        ],
        resize_keyboard=True
    )

def get_cancel_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Отмена')]],
        resize_keyboard=True
    )

def get_main_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Открыть сайт', url='https://google.com')],
            [InlineKeyboardButton(text='Подробнее', callback_data='info_more')]
        ]
    )

# Для удаления клавиатуры (используем напрямую ReplyKeyboardRemove() где нужно)