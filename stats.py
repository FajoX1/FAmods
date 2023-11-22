#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Stats
# Description: Get your account stats
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/stats.png?raw=true
# ---------------------------------------------------------------------------------

from datetime import datetime
import logging

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Stats(loader.Module):
    """Get your account stats"""

    strings = {
        "name": "Stats",
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

    @loader.command()
    async def stats(self, message):
        """Get stats"""

        await utils.answer(message, "<b><emoji document_id=5326015457155620929>🔄</emoji> Загрузка статистики...</b>")
        start = datetime.now()
        u_chat = 0
        b_chat = 0
        c_chat = 0
        ch_chat = 0

        async for dialog in self._client.iter_dialogs():
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

        end = datetime.now()
        ms = (end - start).seconds
        await utils.answer(message,
f"""<b><emoji document_id=5431577498364158238>📊</emoji> Your statistics

<i><emoji document_id=5451732530048802485>⏳</emoji> <code>{ms}</code> seconds</b></i>

<b><emoji document_id=5258011929993026890>👤</emoji> <code>{u_chat}</code> personal chats.</b>
<b><emoji document_id=5258513401784573443>👥</emoji> <code>{c_chat}</code> groups.</b>
<b><emoji document_id=5852471614628696454>📢</emoji> <code>{ch_chat}</code> channels.</b>
<b><emoji document_id=5258093637450866522>🤖</emoji> <code>{b_chat}</code> chat with bots.</b>""")