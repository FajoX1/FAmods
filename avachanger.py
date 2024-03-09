#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: AvaChanger
# Description: Смена аватарки
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/avachanger.png?raw=true
# ---------------------------------------------------------------------------------

import os
import asyncio
import tempfile

import logging

from telethon.tl.functions.photos import UploadProfilePhotoRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class AvaChanger(loader.Module):
    """Смена аватарки"""

    strings = {
        "name": "AvaChanger",

        "no_args": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно <code>{}avatarl [сколько раз] [сколько ждать перед сменой каждой аватарки]</code></b>",
        "no_reply": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно ответить на сообщение с фоткой</b>",

        "changing_avatars": "<emoji document_id=5328274090262275771>🔄</emoji> <b>Меняю аватарки...</b>\n<i>⏳ Это займёт {} секунд</i>",

        "completed": "<b><emoji document_id=5212932275376759608>✅</emoji> Готово. Сменил аватарку {} раз за {} секунд</b>.",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        
    @loader.command()
    async def avatarl(self, message):
        """Смена аватарки по времени"""
        
        args = utils.get_args_raw(message)

        try:
            counts, time_c = args.split(" ")
            counts = int(counts)
            time_c = int(time_c)
        except:
            return await utils.answer(message, self.strings['no_args'].format(self.get_prefix()))
        
        r = await message.get_reply_message()

        if not r:
            return await utils.answer(message, self.strings['no_reply'])
        
        await utils.answer(message, self.strings['changing_avatars'].format((time_c * counts)))

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, os.path.basename("avatar.jpg"))
        
            await message.client.download_media(r.media.photo, file_path)

            for i in range(counts):
                await self.client(UploadProfilePhotoRequest(file=await self.client.upload_file(file_path)))
                await asyncio.sleep(time_c)

        await utils.answer(message, self.strings['completed'].format(counts, (time_c * counts)))