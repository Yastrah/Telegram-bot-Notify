from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


kb_main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_main_menu.add(KeyboardButton('/list'))
kb_main_menu.add(KeyboardButton('/delete'),
                 KeyboardButton('/edit'))

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_cancel.add('/cancel')


inline_kb_confirm = InlineKeyboardMarkup(row_width=2)
inline_kb_confirm.add(InlineKeyboardButton('✅', callback_data='yes'),
                      InlineKeyboardButton('❌', callback_data='no'))


# greet_kb2 = ReplyKeyboardMarkup(
#     resize_keyboard=True, one_time_keyboard=True
# )


