#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: RemoveBG
# Description: Убрать фон из изображения
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/removebg.png?raw=true
# requires: requests
# ---------------------------------------------------------------------------------

import os
import tempfile
import logging
import requests

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class RemoveBG(loader.Module):
    """Убрать фон из изображения"""

    strings = {
        "name": "RemoveBG",

        "must_be_forced": "<emoji document_id=5854929766146118183>❌</emoji> <b>Фото не должно быть сжатим!</b>",
        "no_photo": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нужно ответить на фото!</b>",
        "no_token": "<emoji document_id=5854929766146118183>❌</emoji> <b>Нету токена! Поставь его в <code>{}cfg RemoveBG</code></b>",
        "invalid_token": "<b>😕 Неверный токен</b>",
        "only_photo": "<b>😕 Удалять фон можно только с фото (.png, .jpg, .jpeg)</b>",

        "removing_bg": "<emoji document_id=5326015457155620929>🔄</emoji> <b>Удаление фона...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "api_token",
                None,
                lambda: "Токен для работы с API. Взять можно на сайте https://www.remove.bg/dashboard#api-key",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        # morisummermods feature
        try:
            channel = await self.client.get_entity("t.me/famods")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.error("Can't join @famods")

    @loader.command()
    async def removebg(self, message):
        """Убрать фон из изображения"""
        
        reply = await message.get_reply_message()
        if not reply:
            return await utils.answer(message, self.strings("no_photo"))
        
        try:
            if not any(ext in reply.file.name for ext in [".png", ".jpg", ".jpeg"]):
              return await utils.answer(message, self.strings['only_photo'])
        except TypeError:
            return await utils.answer(message, self.strings['must_be_forced'])

        if not self.config["api_token"]:
            return await utils.answer(message, self.strings["no_token"].format(self.get_prefix()))

        await utils.answer(message, self.strings['removing_bg'])

        with tempfile.TemporaryDirectory() as temp_dir:
            try:
               file_path = os.path.join(temp_dir, reply.file.name)
               await reply.download_media(file_path)
            except TypeError:
                return await utils.answer(message, self.strings['must_be_forced'])
            
            access_token = self.config["api_token"]
            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(file_path, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': access_token},
            )
            try:
              if response.json()['errors'][0]['title'] == "API Key invalid":
                return await utils.answer(message, self.strings['invalid_token'])
            except:
                pass
            file_namee = f"famods-no-bg-{reply.file.name.replace('.jpg', '').replace('.png', '').replace('.jpeg', '')}.png"
            with open(os.path.join(temp_dir, file_namee), 'wb') as out:
               out.write(response.content)
    
            await message.client.send_file(message.chat_id, os.path.join(temp_dir,file_namee), force_document=True)
            return await message.delete()