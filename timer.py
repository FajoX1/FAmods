#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Timer
# Description: Показывает сколько времени осталось
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/timer.png?raw=true
# ---------------------------------------------------------------------------------

import pytz
import logging
from datetime import datetime

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Timer(loader.Module):
    """Показывает сколько времени осталось"""

    strings = {
        "name": "Timer",

        "no_date": "<b><emoji document_id=5019523782004441717>❌</emoji> Добавь сначала дату в <code>{}cfg timer</code></b>",

        "invalid_date": "<b><emoji document_id=5019523782004441717>❌</emoji> Неверный формат даты и времени в конфиге.</b>",
        "invalid_timezone": "<b><emoji document_id=5019523782004441717>❌</emoji> Неверный часовой пояс.</b>"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text",
                "<b>🕑 Осталось до этого ещё {time}</b>",
                lambda: "Текст который будет отображаться с датой. (Можно использовать HTML-разметку) Пример: 🕑 Осталось до этого ещё {time}",
            ),
            loader.ConfigValue(
                "date",
                None,
                lambda: "Дата до которой нужно считать. Пример: 25.04.2025 17:05",
            ),
            loader.ConfigValue(
                "timezone",
                "auto",
                lambda: "Часовой пояс, по стандарту автоматически. Пример: Europe/Moscow",
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
    async def stime(self, message):
        """Посмотреть сколько осталось времени"""

        if not self.config["date"]:
            return await utils.answer(message, self.strings['no_date'])

        date_time_str = self.config['date']
        timezone = self.config.get('timezone', 'auto')

        try:
            date_str, time_str = date_time_str.split(' ')
        except ValueError:
            return await utils.answer(message, self.strings['invalid_date'])

        day, month, year = map(int, date_str.split("."))
        hour, minute = map(int, time_str.split(":"))

        now = datetime.now()

        if timezone == 'auto':
            event_time = datetime(year, month, day, hour, minute)
        else:
            try:
                user_timezone = pytz.timezone(timezone)
                event_time = user_timezone.localize(datetime(year, month, day, hour, minute))
            except pytz.UnknownTimeZoneError:
                return await utils.answer(message, self.strings['invalid_timezone'])

        if now > event_time.replace(tzinfo=None):
            event_time = datetime(now.year + 1, month, day, hour, minute)
            if timezone != 'auto':
                event_time = user_timezone.localize(event_time)

        if timezone != 'auto' and now.tzinfo != event_time.tzinfo:
            now = now.astimezone(user_timezone)

        time_to_event = abs(event_time - now)
        days = time_to_event.days

        years = days // 365
        days %= 365

        hours, remainder = divmod(time_to_event.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        time_to = ""

        if years > 0:
            time_to += f"{years} {'год' if years == 1 else 'года' if 1 < years < 5 else 'лет'} "

        time_to += f"{days} дней {hours} часов {minutes} минут {seconds} секунд"

        await utils.answer(
            message,
            self.config["text"].format(time=time_to),
        )
