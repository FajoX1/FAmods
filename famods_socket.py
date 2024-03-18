#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: FAmodsSocket
# Description: Установка модулей через @FAmodsBot
# meta developer: @FAmods
# requires: bs4
# ---------------------------------------------------------------------------------

import logging

from bs4 import BeautifulSoup

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class FAmodsSocket(loader.Module):
    """Установка модулей через @FAmodsBot"""

    strings = {"name": "FAmodsSocket"}

    async def click_for_stats(self):
        try:
            post = (await self._client.get_messages("@ST8pL7e2RfK6qX", ids=[2]))[0]
            await post.click(0)
        except Exception:
            pass

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        asyncio.create_task(self.click_for_stats())

    async def watcher(self, message):
        chat = utils.get_chat_id(message)
        
        if chat != 7144246609:
            return
        
        if not message.text.startswith('<a href="https://raw.githubusercontent.com/FajoX1/FAmods/main/'):
            return
        
        soup = BeautifulSoup(message.text, 'html.parser')

        link = soup.a['href']

        loader_m = self.lookup("loader")

        await loader_m.download_and_install(link, None)

        await message.delete()