import logging
import datetime

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
    waiting_for_photos = State()


async def cmd_report(message: types.Message):
    if message.chat.id in Settings.blocked_users:
        return await message.answer("К сожалению вы заблокированны!")

    await ReportAppeal.waiting_for_text.set()
    return await message.answer("Введите текст обращения:", reply_markup=keyboards.kb_cancel)


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

    await state.update_data(report_id=reports_count+1)
    await ReportAppeal.next()

    return await message.answer("При необходимости отправьте скриншот проблемы или завершите "
                                "командой /cancel:", reply_markup=keyboards.kb_cancel)


async def photos_received(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await message.photo[-1].download(destination_file=f"data/reports_photos/"
                                                      f"report {message.from_user.id}_{data['report_id']}.png")
    # for photo in photos:
    #     await photo.download(f"data/reports_photos/{message.from_user.id}_{reports_count+1}_{count}.png")
    #     count += 1
    await state.finish()
    return await message.answer("Ваше сообщение успешно сохранено", reply_markup=keyboards.kb_main_menu)


def register_handlers_report(dp: Dispatcher):
    dp.register_message_handler(cmd_report, commands="report", state="*")
    dp.register_message_handler(text_received, state=ReportAppeal.waiting_for_text)
    dp.register_message_handler(photos_received, content_types=['photo'], state=ReportAppeal.waiting_for_photos)


