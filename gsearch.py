#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Gsearch
# Description: Поиск в Google
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/gsearch.png?raw=true
# requires: google
# ---------------------------------------------------------------------------------

import time
import asyncio
import logging

from googlesearch import search
from urllib.parse import unquote

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Gsearch(loader.Module):
    """Поиск в Google"""

    strings = {
        "name": "Gsearch",

        "no_q": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть .gsearch [запрос]</b>",
        "no_result": "<b>😕 Ничего не нашёл по этому запросу</b>",

        "searching": "<emoji document_id=5326015457155620929>🔄</emoji> <b>Поиск в google.com...</b>",
        "searched": """<b>
<emoji document_id=5308054573938647180>🔍</emoji> Результаты поиска</b>{}

<i>{} результатов за {} сек</i>
</b>""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "results",
                5,
                lambda: "Количество результатов",
            ),
            loader.ConfigValue(
                "safe_search",
                False,
                lambda: "Безопастный поиск",
            ),
            loader.ConfigValue(
                "lang",
                "ru",
                lambda: "Язык результатов",
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

    @loader.command()
    async def gsearch(self, message):
        """Поиск в Google"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(message, self.strings["no_q"])

        await utils.answer(message, self.strings['searching'])

        safe_s = "off"

        if self.config["safe_search"]:
            safe_s = "on"

        count_s = 0

        start_time = time.time()

        searched_result = ""

        for url in search(q, stop=self.config["results"], lang=self.config["safe_search"], safe=safe_s):
           searched_result += f"\n<emoji document_id=5098187078693290864>🔵</emoji> <i>{unquote(url)}</i>"
           count_s += 1

        end_time = time.time()
        execution_time = end_time - start_time
        
        if count_s == 0:
            return await utils.answer(message, self.strings['no_result'])

        return await utils.answer(message, self.strings['searched'].format(searched_result, count_s, execution_time))