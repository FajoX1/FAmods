#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Epsilion
# Description: Авто-фарм в @EpsilionWarBot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/epsilion.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl

import random
import asyncio
import logging

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Epsilion(loader.Module):
    """Авто-фарм в @EpsilionWarBot"""

    strings = {
        "name": "Epsilion",

        "checking_profile": "<b><emoji document_id=5424885441100782420>👀</emoji> Смотрю профиль...</b>",

        "b_on": "<b><emoji document_id=5429633836684157942>⚡️</emoji> Авто-фарм включен!</b>",
        "b_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-фарм выключен!</b>",

        "bonus_on": "<b><emoji document_id=5429633836684157942>⚡️</emoji> Авто ежедневный бонус включен!</b>",
        "bonus_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто ежедневный бонус выключен!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "location",
                "☘️ Фермерские угодья",
                lambda: "Локация в которую ты по стандарту будешь отправляться. Пример: ☘️ Фермерские угодья",
            ),
            loader.ConfigValue(
                "start_message",
                "💖 Ваше здоровье полностью восстановлено",
                lambda: "Сообщение от бота после которого начинается бой",
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

        if self.db.get(self.name, "battle", False):
           asyncio.create_task(self._battle())

    async def _change_location(self, conv, location):
     if location == "default":
        location = self.config['location']
     while True:
      try:
        msg = await self._client.send_message(776510403, "🗺 Карта")
        r = await conv.get_response()
        await msg.delete()
        await r.delete()
        await asyncio.sleep(4.4324232432)
        msg = await self._client.send_message(776510403, location)
        r = await conv.get_response()
        r = await conv.get_response()
        await msg.delete()
        await r.delete()
        break
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _battle(self):
     self.cont = True
     while self.cont:
      try:
        async with self._client.conversation("@EpsilionWarBot") as conv:
            msg = await conv.send_message("⚔️ Найти врагов")
            r = await conv.get_response()
            await msg.delete()
            cavella = False
            cavella = True if not r.text == "🔭 Начался поиск противника" else False
            if "❗️ Недостаточно здоровья для сражений" in r.text:
               return
            if cavella:
                await self._change_location(conv, "default")
                msg = await conv.send_message("⚔️ Найти врагов")
                r = await conv.get_response()
                await msg.delete()
            while self.cont:
                r = await conv.get_response()
                pr = []
                for b in r.reply_markup.rows:
                   for bu in b.buttons:
                    if all(x not in bu.text for x in ["Сбежать", "Пропустить", "(", ")", "[", "]"]):
                        pr.append(bu.text)
                msg = await conv.send_message(random.choice(pr))
                r = await conv.get_response()
                if not "блокировать?" in r.text:
                    if "Тебе не повезло" in r.text:
                        await conv.send_message("💀 Принять участь")
                    if "Ты победил" in r.text:
                        await conv.send_message("✅ Забрать нaграду")
                    self.cont = False
                    return
                await asyncio.sleep(3.54354353)
                pr = []
                for b in r.reply_markup.rows:
                   for bu in b.buttons:
                    if all(x not in bu.text for x in ["Сбежать", "Пропустить", "(", ")", "[", "]"]):
                        pr.append(bu.text)
                msg = await conv.send_message(random.choice(pr))
                r = await conv.get_response()
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _bonus(self):
     self.cont = True
     while self.cont:
      try:
        async with self._client.conversation("@EpsilionWarBot") as conv:
            msg = await conv.send_message("📟 Меню")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            msg = await self._client.send_message(776510403, "🎁 Награды")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            msg = await self._client.send_message(776510403, "🧁  Ежедневная награда")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            break
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    async def _getprofme(self):
     while True:
      try:
        async with self._client.conversation("@EpsilionWarBot") as conv:
            msg = await conv.send_message("/equip")
            r = await conv.get_response()
            await msg.delete()
            await r.delete()
            return f"<b>📁 Профиль</b>\n\n{r.text}"
      except hikkatl.errors.common.AlreadyInConversationError:
          await asyncio.sleep(5.67)

    @loader.command()
    async def eps(self, message):
        """Включить/выключить авто-фарм"""

        if self.db.get(self.name, "battle", False):
            self.cont = False
            self.db.set(self.name, "battle", False)
            return await utils.answer(message, self.strings["b_off"])

        self.db.set(self.name, "battle", True)

        await utils.answer(message, self.strings["b_on"])

        await self._battle()

    @loader.command()
    async def epb(self, message):
        """Включить/выключить авто ежедневный бонус"""

        if self.db.get(self.name, "everyday_bonus", False):
            self.db.set(self.name, "everyday_bonus", False)
            return await utils.answer(message, self.strings["bonus_off"])

        self.db.set(self.name, "everyday_bonus", True)

        await utils.answer(message, self.strings["bonus_on"])

        await self._bonus()
        
    @loader.command()
    async def epp(self, message):
        """Посмотреть свой профиль"""

        await utils.answer(message, self.strings["checking_profile"])

        await utils.answer(message, await self._getprofme())

    @loader.loop(interval=60*60*24, autostart=True)
    async def loop(self):
      if self.db.get(self.name, "everyday_bonus", False):
        await self._bonus()
        await asyncio.sleep(random.randint(65, 90))

    async def watcher(self, event):
        chat = utils.get_chat_id(event)
        
        if chat != 776510403:
            return
        
        if event.raw_text == self.config['start_message']:
            if self.db.get(self.name, "battle", False):
                await asyncio.sleep(random.randint(3, 5))
                asyncio.create_task(await self._battle())

        if all(keyword in event.raw_text for keyword in ["Тебя убил"]):
            self.cont = False
            await self._client.send_message(776510403, "💀 Принять участь")
        
        if all(keyword in event.raw_text for keyword in ["успел от тебя сбежать", "Ты победил", "убивает", "отправляешься в ближайший город на восстановление"]):
            self.cont = False
            await self._client.send_message(776510403, "✅ Забрать нaграду")