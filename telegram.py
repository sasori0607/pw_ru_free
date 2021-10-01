#1001558512226

import asyncio
from my_objects import server
from aiogram import Bot


token = "1951848439:AAE6Gp86G-TVd6RrgJHHf7N1NQN7SEnUF7M"
bot = Bot(token)


async def error():
    if server == 1:
        msg = "Камбека(виртуалка)"
    else:
        msg = "УльтраНью(основной комп)"

    await bot.send_message(306672991 ,"Была сделана перезагрузка "+msg)
    await bot.close()


async def start():
    if server == 1:
        msg = "Камбека(виртуалка)"
    else:
        msg = "УльтраНью(основной комп)"

    await bot.send_message(306672991 ,"Бот стартанул "+msg)
    await bot.close()


def mess_error():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(error())

def mess_start():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start())