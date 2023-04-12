import aiofiles
import logging
import os

from typing import Union, Optional


# читаем записи в блокноте построчно
async def read_file(user_id: int) -> Union[str, Exception]:
    try:
        async with aiofiles.open(f'./notebook/{user_id}.txt', mode='r',
                                 encoding='utf-8') as file:
            lines = []
            lines_id = 1
            async for line in file:
                lines.append(f'{lines_id}-{line}')
                lines_id += 1
            return ''.join(lines)
    except Exception as error:
        logging.info(f'{error}')
        return error


# добавляем новую запись в конец файла
async def write_file(user_id: int, text: str) -> Optional[Exception]:
    try:
        async with aiofiles.open(f'./notebook/{user_id}.txt',
                                 mode='a',
                                 encoding='utf-8') as file:
            await file.write(f'{text}\n')
    except Exception as error:
        logging.info(f'{error}')
        return error


# удаляем запись методом невключения её при перезаписи файла
async def delete_record(user_id: int, text: str) -> Optional[Exception]:
    try:
        async with aiofiles.open(f'./notebook/{user_id}.txt',
                                 mode='r+',
                                 encoding='utf-8') as file:
            lines = await file.readlines()
            await file.seek(0)
            for number, line in enumerate(lines):
                if number != (int(text) - 1):
                    await file.write(line)
            await file.truncate()
    except Exception as error:
        logging.info(f'{error}')
        return error


# проверяем наличие файла при старте бота, если нет - создаём
async def create_file(user_id: int) -> Optional[Exception]:
    try:
        if os.path.isfile(f'./notebook/{user_id}.txt'):
            pass
        else:
            async with aiofiles.open(f'./notebook/{user_id}.txt',
                                     mode='x',
                                     encoding='utf-8') as file:
                await file.close()
    except Exception as error:
        logging.info(f'{error}')
        return error
