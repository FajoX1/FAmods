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

import hikkatl

import random
import asyncio
import logging

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Fabrika(loader.Module):
    """Авто-фарм в @fabrika"""

    strings = {
        "name": "Fabrika",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",

        "rw_on_already": "<b>🗿 Авто отправка рабочих уже включена!</b>",
        "rw_off_already": "<b>🗿 Авто отправка рабочих уже выключена!</b>",

        "team_on_already": "<b>🗿 Авто отправка на комадную работу уже включена!</b>",
        "team_off_already": "<b>🗿 Авто отправка на комадную работу уже выключена!</b>",

        "autobonus_on_already": "<b>🗿 Авто-бонус уже включен!</b>",
        "autobonus_off_already": "<b>🗿 Авто-бонус уже выключен!</b>",

        "rw_on": "<b><emoji document_id=5429633836684157942>⚡️</emoji> Отправка рабочих включена!</b>",
        "rw_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Отправка рабочих выключена!</b>",

        "team_on": "<b><emoji document_id=5429633836684157942>⚡️</emoji> Командная работа включена!</b>",
        "team_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Командная работа выключена!</b>",

        "bonus_on": "<b><emoji document_id=5852779353330421386>🎁</emoji> Авто-бонус включен!</b>",
        "bonus_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-бонус выключен!</b>",
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

    async def _slavesw(self):
     while True:
      try:
        async with self._client.conversation("@fabrika") as conv:
            msg = await conv.send_message("/factory")
            await msg.delete()

            r = await conv.get_response()
            await r.click(1)
            r = await conv.get_edit()
            await r.click(0)
            await r.delete()
            break
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _teamw(self):
     while True:
      try:
        async with self._client.conversation("@fabrika") as conv:
            msg = await conv.send_message("/start")
            await msg.delete()

            r = await conv.get_response()
            await r.click(5)
            r = await conv.get_edit()
            await asyncio.sleep(2.61)
            await r.click(3)
            r = await conv.get_edit()
            await asyncio.sleep(3.61)
            await r.click(0)
            await r.delete()
            break
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _takebonus(self):
     while True:
      try:
        async with self._client.conversation("@fabrika") as conv:
            msg = await conv.send_message("/city")
            await msg.delete()

            r = await conv.get_response()
            await r.click(1)
            r = await conv.get_edit()
            await r.click(0)
            await r.delete()
            break
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

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
    async def teamon(self, message):
        """Начать автоматически отправлятся на комадную работу"""

        status = self.db.get(self.name, "team", False)
        if status:
            return await utils.answer(message, self.strings["team_on_already"])

        self.db.set(self.name, "team", True)

        await utils.answer(message, self.strings["team_on"])

        await self._teamw()

    @loader.command()
    async def teamoff(self, message):
        """Остановить автоматически отправлятся на комадную работу"""

        status = self.db.get(self.name, "team", False)
        if not status:
            return await utils.answer(message, self.strings["team_off_already"])

        self.db.set(self.name, "team", False)

        await utils.answer(message, self.strings["team_off"])
    
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
        if "Командная работа завершена!" in event.raw_text:
          if self.db.get(self.name, "team", False):
            await self._teamw()
