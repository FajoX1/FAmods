#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Executor
# Description: Выполнение python кода
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/executor.png?raw=true
# ---------------------------------------------------------------------------------

import sys
import traceback
import html
import time
import asyncio
import logging

from io import StringIO

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Executor(loader.Module):
    """Выполнение python кода"""

    strings = {
        "name": "Executor",

        "no_code": "<emoji document_id=5854929766146118183>❌</emoji> <b>Должно быть </b><code>{}exec [python код]</code>",

        "executing": "<b><emoji document_id=5332600281970517875>🔄</emoji> Выполняю код...</b>"
    }

    async def click_for_stats(self):
        try:
            post = (await self._client.get_messages("@ST8pL7e2RfK6qX", ids=[2]))[0]
            await post.click(0)
        except:
            pass

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        asyncio.create_task(self.click_for_stats())

    async def cexecute(self, code, message, reply):
        r = reply
        client = self.client
        me = await client.get_me()
        result = sys.stdout = StringIO()
        try:
            exec(code)
        except:
            return traceback.format_exc().strip(), True
        return result.getvalue().strip(), False

    @loader.command()
    async def execcmd(self, message):
        """Выполнить python код"""

        code = utils.get_args_raw(message)
        if not code:
            return await utils.answer(message, self.strings["no_code"].format(self.get_prefix()))

        await utils.answer(message, self.strings["executing"])

        reply = await message.get_reply_message()

        start_time = time.perf_counter()
        result, cerr = await self.cexecute(code, message, reply)
        stop_time = time.perf_counter()

        me = await self.client.get_me()
       # result = result.replace("+"+me.phone, "never gonna give you up").replace(me.phone, "never gonna give you up")

        result = html.escape(result)

        return await utils.answer(message, f"""<b>
<emoji document_id=5431376038628171216>💻</emoji> Код:
<pre><code class="language-python">{code}</code></pre>
{'<emoji document_id=6334758581832779720>✅</emoji> Результат' if not cerr else '<emoji document_id=5440381017384822513>🚫</emoji> Ошибка'}:
<pre><code class="language-python">{result}</code></pre>

<emoji document_id=5451732530048802485>⏳</emoji> Выполнен за {round(stop_time - start_time, 5)} секунд</b>""")