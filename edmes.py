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

from .. import loader, utils

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
            ),
            loader.ConfigValue(
                "wait_to_edit",
                1.2,
                lambda: "Сколько будет ждать секунд перед редактиророванием сообщения.",
            )
        )

    @loader.command()
    async def edmsg(self, message):
        """Редактирует"""

        texts = self.config["edit_texts"]
        w_time = self.config["wait_to_edit"]

        for txt in texts:
            await utils.answer(message, txt)
            await asyncio.sleep(w_time)