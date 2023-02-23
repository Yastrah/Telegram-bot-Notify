from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from config.configuration import Constants


kb_main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_main_menu.add(KeyboardButton(Constants.user_commands["list"]["custom_name"]),
                 KeyboardButton(Constants.user_commands["delete"]["custom_name"]),
                 KeyboardButton(Constants.user_commands["edit"]["custom_name"]),
                 KeyboardButton(Constants.user_commands["undo"]["custom_name"]))
# kb_main_menu.add(KeyboardButton(Constants.user_commands["delete"]["custom_name"]),
#                  KeyboardButton(Constants.user_commands["edit"]["custom_name"]))


kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_cancel.add(Constants.user_commands["cancel"]["custom_name"])


inline_kb_confirm = InlineKeyboardMarkup(row_width=2)
inline_kb_confirm.add(InlineKeyboardButton('✅', callback_data='yes'),
                      InlineKeyboardButton('❌', callback_data='no'))


inline_kb_edit_type = InlineKeyboardMarkup(row_width=2)
inline_kb_edit_type.add(InlineKeyboardButton('🕑 время', callback_data='time'),
                        InlineKeyboardButton('📝 текст', callback_data='text'),
                        InlineKeyboardButton('🕑 время и текст 📝', callback_data='all'))

# greet_kb2 = ReplyKeyboardMarkup(
#     resize_keyboard=True, one_time_keyboard=True
# )


