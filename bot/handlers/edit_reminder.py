import logging

from bot.db.config_reader import load_config

# from aiogram import Dispatcher, types
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup

logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


# class EditReminder(StatesGroup):
#     waiting_for_team_name = State()
#     waiting_for_character_name = State()
#     waiting_for_character_class = State()
#     waiting_for_character_stats = State()
#
#
# async def team_start(message: types.Message):
#     verification = protect.user_already_has_team(message.from_user.id)
#     if verification is not True:
#         logger.debug(f"User: {message.from_user.id}. Team is already exist!")
#         await message.answer(verification)
#         return
#
#     await message.answer("Введите имя команды:")
#     await EditReminder.waiting_for_team_name.set()
#
#
# async def team_name_chosen(message: types.Message, state: FSMContext):
#     verification = protect.team_name(message.text)
#     if verification is not True:
#         logger.debug(f"User: {message.from_user.id}. Invalid characters name!")
#         await message.answer(f"{verification}\nВведите имя команды ещё раз:")
#         return
#
#     await state.update_data(team_name=message.text)
#
#     # Для последовательных шагов можно не указывать название состояния, обходясь next()
#     await EditReminder.next()
#     await message.answer("Теперь выберите имя первого члена команды:")
#
#
# async def team_character_name_chosen(message: types.Message, state: FSMContext):
#     # await state.update_data(team_character_name=message.text)
#
#     # получение рандомного персонажа
#
#     user_data = await state.get_data()
#
#     db.add_team(message.from_user.id, user_data["team_name"], [{"name": message.text, "stats": "None"}])
#
#     await message.answer(f"""Вы создали команду "{user_data["team_name"]}".\n"""
#                          f"Первого члена команды зовут {message.text}.")
#     await state.finish()
#
#
# def register_handlers_team(dp: Dispatcher):
#     dp.register_message_handler(team_start, commands=config.bot_commands.new_team, state="*")
#     dp.register_message_handler(team_name_chosen, state=EditReminder.waiting_for_team_name)
#     dp.register_message_handler(team_character_name_chosen, state=EditReminder.waiting_for_character_name)