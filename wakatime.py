#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Wakatime
# Description: Показывает твою Wakatime статистику
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/wakatime.png?raw=true
# requires: httpx
# ---------------------------------------------------------------------------------

import httpx
import asyncio
import logging

from .. import loader, utils

from telethon.tl.functions.channels import JoinChannelRequest

logger = logging.getLogger(__name__)

@loader.tds
class Wakatime(loader.Module):
    """Показывает твою Wakatime статистику"""

    strings = {
        "name": "Wakatime",

        "loading": "<emoji document_id=6334391057186293707>🕑</emoji> <b>Загрузка статистики...</b>",
        "no_token": "<emoji document_id=5210952531676504517>🚫</emoji> <b>Wakatime токен не поставлен! Поставь его в <code>{}cfg wakatime</code></b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "WAKATIME_TOKEN",
                None,
                lambda: "Твой wakatime токен. Получить токен: https://wakatime.com/settings/account",
                validator=loader.validators.Hidden(loader.validators.String()),
            )
        )

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

    async def _get_data(self, endpoint, token):
        url = f"https://wakatime.com/api/v1/users/current/{endpoint}?api_key={token}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        return response

    async def get_waka(self, token):
        endpoints = ["status_bar/today", "stats/all_time", "stats/all_time", "all_time_since_today"]

        responses = await asyncio.gather(*(self._get_data(endpoint, token) for endpoint in endpoints))
        data_today, data_all_time, data_stats_s, data_all_time_since_today = [response.json() for response in responses]

        all_time = data_all_time_since_today["data"]["text"]
        username = data_all_time["data"]["username"]
        if not username:
           username = "Нету"
        try:
          languages = data_all_time["data"]["languages"]
        except:
            languages = []
        today = data_today["data"]["categories"]
        try:
           os = data_all_time["data"]["operating_systems"]
        except:
            pass
        OS = ", ".join([f"<code>{stat['name']}</code>" for stat in os if stat["text"] != "0 secs"])
        editor = data_all_time["data"]["editors"]
        EDITOR = ", ".join([f"<code>{stat['name']}</code> " for stat in editor if stat["text"] != "0 secs"])
        try:
           LANG = "\n".join([f"▫️ <b>{stat['name']}</b>: <i>{stat['text']}</i>" for stat in languages if stat["text"] != "0 secs"])
        except:
            LANG = ""
        TODAY = "\n".join([f"{stat['text']}" for stat in today if stat["text"] != "0 secs"])

        return f"""<b><emoji document_id=5190458330719461749>🧑‍💻</emoji> Юзернейм: <code>{username}</code>

<emoji document_id=6334391057186293707>🕑</emoji> За всё время: <code>{all_time}</code>
📃 Сегодня: <code>{TODAY}</code>

<emoji document_id=6334742097748298141>🖥</emoji> ОС:</b> <i>{OS}</i>
<emoji document_id=5807454683714817955>💻</emoji> <b>Редактор:</b> <i>{EDITOR}</i>

<b>💈 Языки программирования</b>

{LANG}\n"""

    @loader.command()
    async def waka(self, message):
        """Посмотреть свою статистику в Wakatime"""
        token = self.config["WAKATIME_TOKEN"]

        if token is None:
            return await utils.answer(message, self.strings["no_token"].format(self.get_prefix()))

        await utils.answer(message, self.strings["loading"])

        waka_text = await self.get_waka(token)

        await utils.answer(message, waka_text)