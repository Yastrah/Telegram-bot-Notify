import logging
import datetime
import re

from config.config_reader import load_config
from config.configuration import Settings

from bot import keyboards

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


logger = logging.getLogger(__name__)
config = load_config("config/bot.ini")


class ReportAppeal(StatesGroup):
    waiting_for_text = State()


async def cmd_report(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in Settings.blocked_users:
        return await message.answer("🔒 К сожалению вы заблокированны!")

    with open("data/reports.txt", mode='r', encoding="utf-8") as file:
        file.readline()
        data = file.read()

    if data:
        now_date = datetime.datetime.now().strftime("%Y-%m-%d")
        pattern = re.compile(fr"{now_date}.+?{message.from_user.id}")
        match = pattern.findall(data)

        if len(match) >= Settings.max_reports_per_day:
            return await message.answer(f"Вы за сегодня уже отправили максимальное допустимое число "
                                        f"жалоб/предложений ({Settings.max_reports_per_day})!")

    await ReportAppeal.waiting_for_text.set()
    return await message.answer("Введите, как можно более подробный, текст обращения:", reply_markup=keyboards.kb_cancel)


async def text_received(message: types.Message, state: FSMContext):
    with open("data/reports.txt", mode='r', encoding="utf-8") as file:
        reports_count = int(file.readline())
        data = file.readlines()

    now_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"{now_date} [report] id={message.from_user.id}_{reports_count+1}: {message.text}\n"

    with open("data/reports.txt", mode='w', encoding="utf-8") as file:
        file.writelines([f"{reports_count+1}\n"]+data+[report])

    logger.warning(f"Appeal received from report_id: {message.from_user.id}_{reports_count+1}")

    if data:
        if data[-1].split()[0] != now_date.split()[0]:
            for admin in config.bot.admin_id:
                await message.bot.send_message(chat_id=admin, text="Appeal received")

    await state.finish()
    return await message.answer("Ваше сообщение успешно сохранено", reply_markup=keyboards.kb_main_menu)


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(cmd_report, commands="report", state="*")
    dp.register_message_handler(text_received, state=ReportAppeal.waiting_for_text)


