from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from config.configuration import Constants


kb_remove = ReplyKeyboardRemove()

kb_main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
kb_main_menu.add(KeyboardButton(Constants.user_commands["list"]["custom_name"]),
                 KeyboardButton(Constants.user_commands["delete"]["custom_name"]),
                 KeyboardButton(Constants.user_commands["edit"]["custom_name"]),
                 KeyboardButton(Constants.user_commands["undo"]["custom_name"]))
# kb_main_menu.add(KeyboardButton(Constants.user_commands["delete"]["custom_name"]),
#                  KeyboardButton(Constants.user_commands["edit"]["custom_name"]))

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_cancel.add(Constants.user_commands["menu"]["custom_name"])

inline_kb_language = InlineKeyboardMarkup(row_width=2)
inline_kb_language.add(InlineKeyboardButton('text', callback_data='ru'),
                       InlineKeyboardButton('text', callback_data='en'))

inline_kb_confirm = InlineKeyboardMarkup(row_width=2)
inline_kb_confirm.add(InlineKeyboardButton('✅', callback_data='yes'),
                      InlineKeyboardButton('❌', callback_data='no'))


inline_kb_edit_type = InlineKeyboardMarkup(row_width=2)
inline_kb_edit_type.add(InlineKeyboardButton('🕑 время', callback_data='time'),
                        InlineKeyboardButton('📝 текст', callback_data='text'),
                        InlineKeyboardButton('🕑 время и текст 📝', callback_data='all'))

inline_kb_edit_settings = InlineKeyboardMarkup(row_width=2)
inline_kb_edit_settings.add(InlineKeyboardButton('часовой пояс', callback_data='edit_time_zone'))

inline_kb_utc = InlineKeyboardMarkup(row_width=4)
inline_kb_utc.add(
    InlineKeyboardButton('-10:00', callback_data='utc -10:00'),
    InlineKeyboardButton('-09:00', callback_data='utc -09:00'),
    InlineKeyboardButton('-08:00', callback_data='utc -08:00'),
    InlineKeyboardButton('-07:00', callback_data='utc -07:00'),
    InlineKeyboardButton('-06:00', callback_data='utc -06:00'),
    InlineKeyboardButton('-05:00', callback_data='utc -05:00'),
    InlineKeyboardButton('-04:00', callback_data='utc -04:00'),
    InlineKeyboardButton('-03:00', callback_data='utc -03:00'),
    InlineKeyboardButton('-02:00', callback_data='utc -02:00'),
    InlineKeyboardButton('-01:00', callback_data='utc -01:00'),
    InlineKeyboardButton('00:00', callback_data='utc ±00:00'),
    InlineKeyboardButton('+01:00', callback_data='utc +01:00'),
    InlineKeyboardButton('+02:00', callback_data='utc +02:00'),
    InlineKeyboardButton('+03:00', callback_data='utc +03:00'),
    InlineKeyboardButton('+04:00', callback_data='utc +04:00'),
    InlineKeyboardButton('+05:00', callback_data='utc +05:00'),
    InlineKeyboardButton('+06:00', callback_data='utc +06:00'),
    InlineKeyboardButton('+07:00', callback_data='utc +07:00'),
    InlineKeyboardButton('+08:00', callback_data='utc +08:00'),
    InlineKeyboardButton('+09:00', callback_data='utc +09:00'),
    InlineKeyboardButton('+10:00', callback_data='utc +10:00'),
    InlineKeyboardButton('+11:00', callback_data='utc +11:00'),
    InlineKeyboardButton('+12:00', callback_data='utc +12:00'),
    InlineKeyboardButton('+13:00', callback_data='utc +13:00'),
)


def inline_kb_id_list(id_list: list) -> InlineKeyboardMarkup:
    row_width = 4
    if len(id_list) % 4 < 3:
        row_width = 3

    inline_kb = InlineKeyboardMarkup(row_width=row_width)
    buttons = [InlineKeyboardButton(str(id), callback_data=(str(id))) for id in id_list]
    inline_kb.add(*buttons)
    return inline_kb

# greet_kb2 = ReplyKeyboardMarkup(
#     resize_keyboard=True, one_time_keyboard=True
# )


