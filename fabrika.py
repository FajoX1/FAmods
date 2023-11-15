#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Fabrika
# Description: Autofarm in @fabrika
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/fabrika.png?raw=true
# ---------------------------------------------------------------------------------

import random
import asyncio

from .. import loader, utils

@loader.tds
class Fabrika(loader.Module):
    """Авто-фарм в @fabrika"""

    strings = {
        "name": "Fabrika",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",

        "rw_on_already": "<b>🗿 Авто отправка рабочих уже включена!</b>",
        "rw_off_already": "<b>🗿 Авто отправка рабочих уже выключена!</b>",

        "autobonus_on_already": "<b>🗿 Авто-бонус уже включен!</b>",
        "autobonus_off_already": "<b>🗿 Авто-бонус уже выключен!</b>",

        "rw_on": "<b><emoji document_id=5429633836684157942>⚡️</emoji> Отправка рабочих включена!</b>",
        "rw_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Отправка рабочих выключена!</b>",

        "bonus_on": "<b><emoji document_id=5852779353330421386>🎁</emoji> Авто-бонус включен!</b>",
        "bonus_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-бонус выключен!</b>",
    }

    async def _slavesw(self):
        async with self._client.conversation("@fabrika") as conv:
            msg = await conv.send_message("/factory")
            await msg.delete()

            r = await conv.get_response()
            await r.click(1)
            r = await conv.get_edit()
            await r.click(0)
            await r.delete()

    async def _takebonus(self):
        async with self._client.conversation("@fabrika") as conv:
            msg = await conv.send_message("/city")
            await msg.delete()

            r = await conv.get_response()
            await r.click(1)
            r = await conv.get_edit()
            await r.click(0)
            await r.delete()

    @loader.command()
    async def rwon(self, message):
        """Начать автоматически давать работу работникам"""

        status = self.db.get(self.name, "slaves_w", False)
        if status:
            return await utils.answer(message, self.strings["rw_on_already"])

        self.db.set(self.name, "slaves_w", True)

        await utils.answer(message, self.strings["rw_on"])

        await self._slavesw()

    @loader.command()
    async def rwoff(self, message):
        """Остановить автоматически давать работу работникам"""

        status = self.db.get(self.name, "slaves_w", False)
        if not status:
            return await utils.answer(message, self.strings["rw_off_already"])

        self.db.set(self.name, "slaves_w", False)

        await utils.answer(message, self.strings["rw_off"])

    @loader.command()
    async def bonuson(self, message):
        """Начать автоматическое получать бонус"""

        status = self.db.get(self.name, "autobonus", False)
        if status:
            return await utils.answer(message, self.strings["autobonus_on_already"])

        self.db.set(self.name, "autobonus", True)

        await utils.answer(message, self.strings["bonus_on"])

        await self._takebonus()

    @loader.command()
    async def bonusoff(self, message):
        """Остановить автоматическое получение бонуса"""

        status = self.db.get(self.name, "autobonus", False)
        if not status:
            return await utils.answer(message, self.strings["autobonus_off_already"])

        self.db.set(self.name, "autobonus", False)

        await utils.answer(message, self.strings["bonus_off"])
    
    @loader.command()
    async def sprof(self, message):
        """Посмотреть свой профиль"""

        await utils.answer(message, self.strings["checking_profile"])
        async with self._client.conversation("@fabrika") as conv:
            msg = await conv.send_message("/profile")
            await msg.delete()
            r = await conv.get_response()
            await r.delete()
            await utils.answer(message, f"<b>📁 {r.text}</b>")

    @loader.loop(interval=60*60*24, autostart=True)
    async def loop(self):
      if self.db.get(self.name, "autobonus", False):
        await asyncio.sleep(random.randint(65, 90))
        await self._takebonus()

    async def watcher(self, event):
        chat = utils.get_chat_id(event)
        
        if chat != 6520131495:
            return
        
        if all(keyword in event.raw_text for keyword in ["Ваши рабочие", "законч", "работу"]):
          if self.db.get(self.name, "slaves_w", False):
            await self._slavesw()