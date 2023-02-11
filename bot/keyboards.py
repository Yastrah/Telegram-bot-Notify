from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_kb_confirm = InlineKeyboardMarkup(row_width=1)
buttons = [
    InlineKeyboardButton('✅', callback_data='yes'),
    InlineKeyboardButton('❌', callback_data='no')
]
inline_kb_confirm.add(*buttons)


