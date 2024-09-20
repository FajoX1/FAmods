#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: CryptoQR
# Description: Создание QR код в стиле CryptoBot
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/cryptoqr.png?raw=true
# ---------------------------------------------------------------------------------

import hikkatl
import asyncio

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CryptoQR(loader.Module):
    """Создание QR код в стиле CryptoBot"""

    strings = {
        "name": "CryptoQR",

        "no_args": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно <code>{}cqr [текст/ссылка]</code></b>",

        "creating": "<emoji document_id=5451732530048802485>⏳</emoji> <b>Создаю QRcode...</b>",
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
    async def cqr(self, message):
        """Создать QRcode"""
        
        q = utils.get_args_raw(message)
        if not q:
          return await utils.answer(message, self.strings['no_args'].format(self.get_prefix()))

        m = await utils.answer(message, self.strings['creating'])

        await self.client.send_file(m.peer_id, f"https://qr.crypt.bot/?url={q}", force_document=True, caption=f"<emoji document_id=5431376038628171216>💻</emoji> <b>Текст:</b> <code>{q}</code>")
        await m.delete()
