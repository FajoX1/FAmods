#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Wakatime
# Description: Show your Wakatime stats
# meta developer: @FAmods
# meta banner: 
# requires: httpx
# ---------------------------------------------------------------------------------

import httpx
import asyncio

from .. import loader, utils
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest

@loader.tds
class Wakatime(loader.Module):
    """Show your Wakatime stats"""

    strings = {
        "name": "Wakatime",
        "no_token": "<emoji document_id=5210952531676504517>🚫</emoji> <b>Wakatime token not set!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "WAKATIME_TOKEN",
                None,
                lambda: "Your wakatime token",
            )
        )

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
        languages = data_all_time["data"]["languages"]
        today = data_today["data"]["categories"]
        os = data_all_time["data"]["operating_systems"]
        OS = ", ".join([f"<code>{stat['name']}</code>" for stat in os if stat["text"] != "0 secs"])
        editor = data_all_time["data"]["editors"]
        EDITOR = ", ".join([f"<code>{stat['name']}</code> " for stat in editor if stat["text"] != "0 secs"])
        LANG = "\n".join([f"▫️ <b>{stat['name']}</b>: <i>{stat['text']}</i>" for stat in languages if stat["text"] != "0 secs"])
        TODAY = "\n".join([f"{stat['text']}" for stat in today if stat["text"] != "0 secs"])

        return f"""
🧑‍💻 <b>Username:</b> <code>{username}</code>

🕑 <b>All time</b>: <code>{all_time}</code>
📃 <b>Today</b>: <code>{TODAY}</code>

🖥 <b>OS:</b> <i>{OS}</i>
💻 <b>Editor:</b> <i>{EDITOR}</i>

<b>💈 Languages</b>

{LANG}\n"""

    @loader.command()
    async def waka(self, message):
        """See your stats in Wakatime"""
        token = self.config["WAKATIME_TOKEN"]

        if token is None:
            return await utils.answer(message, self.strings["no_token"])

        waka_text = await self.get_waka(token)

        await utils.answer(message, waka_text)