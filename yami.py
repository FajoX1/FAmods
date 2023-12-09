#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Yami
# Description: Автоматизированная работа с @YamiChat_bot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/yami.png?raw=true
# ---------------------------------------------------------------------------------

import random
import asyncio
import logging

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Yami(loader.Module):
    """Автоматизированная работа с @YamiChat_bot"""

    strings = {
        "name": "Yami",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",

        "autofarm_on": "<b><emoji document_id=5427009714745517609>✅</emoji> Авто-фарм включен!</b>",
        "autofarm_off": "<b><emoji document_id=5440381017384822513>❌</emoji> Авто-фарм выключен!</b>",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        # morisummermods feature
        try:
            channel = await self.client.get_entity("t.me/famods")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.error("Can't join @famods")

        try:
            channel = await self.client.get_entity("t.me/YamiChannel")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.error("Can't join @YamiChannel")

    async def _farm_ymoney(self):
        async with self._client.conversation("@YamiChat_bot") as conv:
            msg = await conv.send_message("фарм")
            await asyncio.sleep(random.randint(5, 8))
            await msg.delete()

    @loader.command()
    async def yfarm(self, message):
        """Включить/выключить авто-фарм в @YamiChat_bot"""

        status = self.db.get(self.name, "autofarm", False)
        if status:
            self.db.set(self.name, "autofarm", False)
            return await utils.answer(message, self.strings["autofarm_off"])

        self.db.set(self.name, "autofarm", True)

        await utils.answer(message, self.strings["autofarm_on"])

        await self._farm_ymoney()

    @loader.command()
    async def yprof(self, message):
        """Посмотреть свой профиль в @YamiChat_bot"""

        await utils.answer(message, self.strings["checking_profile"])
        async with self._client.conversation("@YamiChat_bot") as conv:
            msg = await conv.send_message(random.choice(["баланс", "кэш", "кеш"]))
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            await utils.answer(message, f"<b>{r.text}</b>")

    @loader.loop(interval=60*60, autostart=True)
    async def loop(self):
      if self.db.get(self.name, "autofarm", False):
        await asyncio.sleep(random.randint(65, 100))
        await self._farm_ymoney()
