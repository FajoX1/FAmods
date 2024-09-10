#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Stats
# Description: Показывает статистику твоего аккаунта
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/stats.png?raw=true
# ---------------------------------------------------------------------------------

import asyncio
from datetime import datetime
import logging

from .. import loader, utils

from telethon.tl.functions.channels import JoinChannelRequest

logger = logging.getLogger(__name__)

@loader.tds
class Stats(loader.Module):
    """Показывает статистику твоего аккаунта"""

    strings = {
        "name": "Stats",

        "loading_stats": "<b><emoji document_id=5326015457155620929>🔄</emoji> Загрузка статистики...</b>",
    }

    async def click_for_stats(self):
        try:
            post = (await self._client.get_messages("@famods_click", ids=[2]))[0]
            await post.click(0)
        except:
            pass

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        try:
            channel = await self.client.get_entity("t.me/famods")
            await client(JoinChannelRequest(channel))
        except Exception:
            logger.error("Can't join @famods")
        asyncio.create_task(self.click_for_stats())

    @loader.command()
    async def stats(self, message):
        """Получить статистику"""

        await utils.answer(message, self.strings['loading_stats'])
        u_chat = 0
        b_chat = 0
        c_chat = 0
        ch_chat = 0
        all_chats = 0

        async for dialog in self._client.iter_dialogs():
            all_chats += 1
            if dialog.is_user:
                if dialog.entity.bot:
                    b_chat += 1
                elif not dialog.entity.bot:
                    u_chat += 1
            elif dialog.is_group:
                c_chat += 1
            elif dialog.is_channel:
                if dialog.entity.megagroup or dialog.entity.gigagroup:
                    if dialog.entity.megagroup:
                        c_chat += 1
                    elif dialog.entity.gigagroup:
                        c_chat += 1
                elif not dialog.entity.megagroup and not dialog.entity.gigagroup:
                    ch_chat += 1
        await utils.answer(message,
f"""<b><emoji document_id=5431577498364158238>📊</emoji> Твоя статистика

<emoji document_id=5884510167986343350>💬</emoji> Всего чатов: <code>{all_chats}</code>

<emoji document_id=5258011929993026890>👤</emoji> <code>{u_chat}</code> личных чатов
<emoji document_id=5258513401784573443>👥</emoji> <code>{c_chat}</code> групп
<emoji document_id=5852471614628696454>📢</emoji> <code>{ch_chat}</code> каналов
<emoji document_id=5258093637450866522>🤖</emoji> <code>{b_chat}</code> ботов</b>""")