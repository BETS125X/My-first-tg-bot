import datetime
import os

from aiogram.types import FSInputFile
from PIL import Image

from aiogram import types, Bot

from Bot.running import BOT_TOKEN, SUPPORTED_FORMATS

bot = Bot(token=BOT_TOKEN)


async def convert_image(message: types.Message):
    current_time = datetime.datetime.now().time()
    print(f'    Информация о пользователе: {message.from_user}')
    print(f'Время отправки сообщения пользователем: {current_time}')
    print(f'Пользователь использовал конвертацию в {SUPPORTED_FORMATS}')
    try:
        # получаем желаемый формат из подписи
        desired_format = message.caption.upper()
        if desired_format not in SUPPORTED_FORMATS:
            await message.reply(f'Неподдерживаемый формат. Используйте один из: {', '.join(SUPPORTED_FORMATS)}')
            return

        if not os.path.exists('../Bot/temp'):
            os.makedirs('/Bot/temp')

        # cкачиваем файл
        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, f'temp/input_image')

        else:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            await bot.download_file(file.file_path, f'temp/input_image')

        # конвертируем изображение
        with Image.open('temp/input_image') as img:
            output_path = f'temp/converted_file_image.{desired_format.lower()}'
            img.save(output_path, format=desired_format)

        # отправляем конвертированное изображение
        converted_file = FSInputFile(output_path)
        await message.reply_document(converted_file)

        # удаляем временные файлы
        os.remove('temp/input_image')
        os.remove(output_path)

    except Exception as e:
        await message.reply(f'Произошла ошибка при конвертации: {str(e)}')
