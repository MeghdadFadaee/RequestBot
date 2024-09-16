from datetime import datetime, timezone
from jdatetime import datetime as jdatetime
import time
import json
import os

from balethon import Client
from balethon.objects.chat import Chat
from balethon.objects.message import Message

from BeautifulJWT import BeautifulJWT, JWTDecodeError
from BeautifulRequest import is_request, convert_request_to_dict

DATA_CHAT_ID = 5117523172
bot = Client(os.environ.get('BOT_TOKEN'))
chat_ids = []


async def save_chat(chat: Chat) -> None:
    if chat.id not in chat_ids:
        await bot.send_message(DATA_CHAT_ID, f'{chat.id}')
        chat_ids.append(chat.id)

def create_readable_time(unix_time: int) -> str:
  unix_time = int(message.text)
  date_time = datetime.fromtimestamp(unix_time, timezone.utc)
  jalali_date_time = jdatetime.fromtimestamp(unix_time)
  return f'{date_time:%Y-%m-%d %H:%M:%S}\n{jalali_date_time:%Y-%m-%d %H:%M:%S}'


@bot.on_message()
async def greet(message: Message):
    if message.text.lower() == 'ping':
        await message.reply("Pong")
        return None
    if message.text.lower() == 'now':
        unix_time = time.time()
        await message.reply(f'{unix_time}\n' + create_readable_time(unix_time))
        return None

    if is_request(message.text):
        request_dict: dict = convert_request_to_dict(message.text)
        await message.reply(json.dumps(request_dict, ensure_ascii=False, indent=4))
        return None

    if BeautifulJWT.is_jwt_token(message.text):
        try:
            jwt_dict: dict = BeautifulJWT.decode_without_verify(message.text)
            await message.reply(json.dumps(jwt_dict, ensure_ascii=False, indent=4))
        except JWTDecodeError:
            await message.reply('token is invalid.')
        return None

    if message.text.isnumeric() and len(message.text) == 10:
        unix_time = int(message.text)
        await message.reply(create_readable_time(unix_time))
        return None

    if message.text.isnumeric():
        await message.reply(f'{int(message.text) + 4}')
        return None


bot.run()
