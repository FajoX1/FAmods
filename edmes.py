#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Edmes
# Description: Редактирует сообщение с заданим текстом.
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/edmes.png?raw=true
# ---------------------------------------------------------------------------------

import asyncio
import logging

from .. import loader, utils

from telethon.tl.functions.channels import JoinChannelRequest

logger = logging.getLogger(__name__)

@loader.tds
class Edmes(loader.Module):
    """Редактирует сообщение с заданим текстом."""

    strings = {
        "name": "Edmes",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "edit_texts",
                ['👋 Привет', '👨 Я', '✏️ Редактирую', '📋 Текст', '❌ Конец.'],
                lambda: "Текст который будет при редактировании сообщения\nПример: ['👋 Привет', '👨 Я', '✏️ Редактирую', '📋 Текст', '❌ Конец.']",
                validator=loader.validators.Series()
            ),
            loader.ConfigValue(
                "wait_to_edit",
                1.2,
                lambda: "Сколько будет ждать секунд перед редактиророванием сообщения.",
            )
        )

    async def click_for_stats(self):
        try:
            post = (await self._client.get_messages("@famods_click", ids=[2]))[0]
            await post.click(0)
        except:
            pass

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        
        asyncio.create_task(self.click_for_stats())

    @loader.command()
    async def edmsg(self, message):
        """Редактировать"""

        for txt in self.config["edit_texts"]:
            await utils.answer(message, txt)
            await asyncio.sleep(self.config["wait_to_edit"])