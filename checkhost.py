#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: CheckHost
# Description: Проверка доступности веб-сайтов, серверов, хостов и IP-адресов с разных геолокаций и тд.
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/checkhost.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import asyncio
import aiohttp
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CheckHost(loader.Module):
    """Проверка доступности веб-сайтов, серверов, хостов и IP-адресов с разных геолокаций и тд."""

    strings = {
        "name": "CheckHost",

        "no_url": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно <code>{}{} [адрес]</code></b>",

        "checking_http": "<emoji document_id=6332573220868196043>🕓</emoji> <b>Проверяю доступность...</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "limit",
                True,
                lambda: "Включить/Выключить лимит геолокаций в проверке.",
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "limit_geo",
                10,
                lambda: "Лимит геолокаций.",
            ),
        )


    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        
    @loader.command()
    async def chhttp(self, message):
        """Проверить доступность"""
        
        query = utils.get_args_raw(message)

        if not query:
            return await utils.answer(message, self.strings['no_url'].format(self.get_prefix(), 'chhttp'))

        await utils.answer(message, self.strings['checking_http'])

        url_cr = f"https://check-host.net/check-http?host={query}"

        if self.config['limit']:
            url_cr += f"&max_nodes={self.config['limit_geo']}"

        async with aiohttp.ClientSession() as session:
            cr = await session.get(url_cr, headers={'Accept': 'application/json'})
            create = await cr.json()
            await asyncio.sleep(10)
            res = await session.get(f"https://check-host.net/check-result/{create['request_id']}", headers={'Accept': 'application/json'})
            response = await res.json()

        txt = f"""<b>
🌐 Проверка доступности

📡 IP: <code>{list(response.items())[0][1][0][4]}</code>
🔗 Адрес: {query}

🛜 Доступность
</b>
"""

        k = 0

        for inf in create['nodes'].items():
            if self.config['limit']:
                if k == self.config['limit_geo']:
                    break
            country = inf[1][1]
            country_code = inf[1][0]
            try:
                txt += self.flags[country_code] + " "
            except:
                pass
            city = inf[1][2]
            ip = inf[1][3]

            response_code = list(response.items())[k][1][0][3]
            responsee = list(response.items())[k][1][0][2]
            response_seconds = list(response.items())[k][1][0][1]

            txt += f"""<b>{country} ({city}) (<code>{ip}</code>)</b>
<i>Response code: {response_code} ({responsee}) {response_seconds} сек.</i>
"""

            k += 1

        txt += f"\n<b><a href={create['permanent_link']}>🖥 Ссылка на результат в check-host.net</a></b>"
            
        return await utils.answer(message, txt)
    
    flags = {
    "ad": "🇦🇩",  # Андорра
    "ae": "🇦🇪",  # ОАЭ
    "af": "🇦🇫",  # Афганистан
    "ag": "🇦🇬",  # Антигуа и Барбуда
    "ai": "🇦🇮",  # Ангилья
    "al": "🇦🇱",  # Албания
    "am": "🇦🇲",  # Армения
    "ao": "🇦🇴",  # Ангола
    "aq": "🇦🇶",  # Антарктика
    "ar": "🇦🇷",  # Аргентина
    "at": "🇦🇹",  # Австрия
    "au": "🇦🇺",  # Австралия
    "aw": "🇦🇼",  # Аруба
    "ax": "🇦🇽",  # Аландские острова
    "az": "🇦🇿",  # Азербайджан
    "ba": "🇧🇦",  # Босния и Герцеговина
    "bb": "🇧🇧",  # Барбадос
    "bd": "🇧🇩",  # Бангладеш
    "be": "🇧🇪",  # Бельгия
    "bf": "🇧🇫",  # Буркина-Фасо
    "bg": "🇧🇬",  # Болгария
    "bh": "🇧🇭",  # Бахрейн
    "bi": "🇧🇮",  # Бурунди
    "bj": "🇧🇯",  # Бенин
    "bl": "🇧🇱",  # Сен-Бартельми
    "bm": "🇧🇲",  # Бермудские острова
    "bn": "🇧🇳",  # Бруней
    "bo": "🇧🇴",  # Боливия
    "bq": "🇧🇶",  # Бонэйр, Синт-Эстатиус и Саба
    "br": "🇧🇷",  # Бразилия
    "bs": "🇧🇸",  # Багамы
    "bt": "🇧🇹",  # Бутан
    "bv": "🇧🇻",  # остров Буве
    "bw": "🇧🇼",  # Ботсвана
    "by": "🇧🇾",  # Беларусь
    "bz": "🇧🇿",  # Белиз
    "ca": "🇨🇦",  # Канада
    "cc": "🇨🇨",  # Кокосовые (Килинг) острова
    "cd": "🇨🇩",  # Конго - Киншаса
    "cf": "🇨🇫",  # Центральноафриканская Республика
    "cg": "🇨🇬",  # Конго - Браззавиль
    "ch": "🇨🇭",  # Швейцария
    "ci": "🇨🇮",  # Кот-д’Ивуар
    "ck": "🇨🇰",  # Острова Кука
    "cl": "🇨🇱",  # Чили
    "cm": "🇨🇲",  # Камерун
    "cn": "🇨🇳",  # Китай
    "co": "🇨🇴",  # Колумбия
    "cr": "🇨🇷",  # Коста-Рика
    "cu": "🇨🇺",  # Куба
    "cv": "🇨🇻",  # Кабо-Верде
    "cw": "🇨🇼",  # Кюрасао
    "cx": "🇨🇽",  # остров Рождества
    "cy": "🇨🇾",  # Кипр
    "cz": "🇨🇿",  # Чехия
    "de": "🇩🇪",  # Германия
    "dj": "🇩🇯",  # Джибути
    "dk": "🇩🇰",  # Дания
    "dm": "🇩🇲",  # Доминика
    "do": "🇩🇴",  # Доминиканская Республика
    "dz": "🇩🇿",  # Алжир
    "ec": "🇪🇨",  # Эквадор
    "ee": "🇪🇪",  # Эстония
    "eg": "🇪🇬",  # Египет
    "eh": "🇪🇭",  # Западная Сахара
    "er": "🇪🇷",  # Эритрея
    "es": "🇪🇸",  # Испания
    "et": "🇪🇹",  # Эфиопия
    "fi": "🇫🇮",  # Финляндия
    "fj": "🇫🇯",  # Фиджи
    "fk": "🇫🇰",  # Фолклендские острова
    "fm": "🇫🇲",  # Микронезия
    "fo": "🇫🇴",  # Фарерские острова
    "fr": "🇫🇷",  # Франция
    "ga": "🇬🇦",  # Габон
    "gb": "🇬🇧",  # Великобритания
    "gd": "🇬🇩",  # Гренада
    "ge": "🇬🇪",  # Грузия
    "gf": "🇬🇫",  # Французская Гвиана
    "gg": "🇬🇬",  # Гернси
    "gh": "🇬🇭",  # Гана
    "gi": "🇬🇮",  # Гибралтар
    "gl": "🇬🇱",  # Гренландия
    "gm": "🇬🇲",  # Гамбия
    "gn": "🇬🇳",  # Гвинея
    "gp": "🇬🇵",  # Гваделупа
    "gq": "🇬🇶",  # Экваториальная Гвинея
    "gr": "🇬🇷",  # Греция
    "gs": "🇬🇸",  # Южная Георгия и Южные Сандвичевы острова
    "gt": "🇬🇹",  # Гватемала
    "gu": "🇬🇺",  # Гуам
    "gw": "🇬🇼",  # Гвинея-Бисау
    "gy": "🇬🇾",  # Гайана
    "hk": "🇭🇰",  # Гонконг
    "hm": "🇭🇲",  # остров Херд и острова Макдональд
    "hn": "🇭🇳",  # Гондурас
    "hr": "🇭🇷",  # Хорватия
    "ht": "🇭🇹",  # Гаити
    "hu": "🇭🇺",  # Венгрия
    "id": "🇮🇩",  # Индонезия
    "ie": "🇮🇪",  # Ирландия
    "il": "🇮🇱",  # Израиль
    "im": "🇮🇲",  # остров Мэн
    "in": "🇮🇳",  # Индия
    "io": "🇮🇴",  # Британская территория в Индийском океане
    "iq": "🇮🇶",  # Ирак
    "ir": "🇮🇷",  # Иран
    "is": "🇮🇸",  # Исландия
    "it": "🇮🇹",  # Италия
    "je": "🇯🇪",  # Джерси
    "jm": "🇯🇲",  # Ямайка
    "jo": "🇯🇴",  # Иордания
    "jp": "🇯🇵",  # Япония
    "ke": "🇰🇪",  # Кения
    "kg": "🇰🇬",  # Киргизия
    "kh": "🇰🇭",  # Камбоджа
    "ki": "🇰🇮",  # Кирибати
    "km": "🇰🇲",  # Коморы
    "kn": "🇰🇳",  # Сент-Китс и Невис
    "kp": "🇰🇵",  # Корейская Народно-Демократическая Республика
    "kr": "🇰🇷",  # Республика Корея
    "kw": "🇰🇼",  # Кувейт
    "ky": "🇰🇾",  # Каймановы острова
    "kz": "🇰🇿",  # Казахстан
    "la": "🇱🇦",  # Лаос
    "lb": "🇱🇧",  # Ливан
    "lc": "🇱🇨",  # Сент-Люсия
    "li": "🇱🇮",  # Лихтенштейн
    "lk": "🇱🇰",  # Шри-Ланка
    "lr": "🇱🇷",  # Либерия
    "ls": "🇱🇸",  # Лесото
    "lt": "🇱🇹",  # Литва
    "lu": "🇱🇺",  # Люксембург
    "lv": "🇱🇻",  # Латвия
    "ly": "🇱🇾",  # Ливия
    "my": "🇲🇾",
    "md": "🇲🇩",
    "mv": "🇲🇻",
    "mw": "🇲🇼",
    "mx": "🇲🇽",
    "my": "🇲🇾",
    "mz": "🇲🇿",
    "na": "🇳🇦",
    "nc": "🇳🇨",
    "ne": "🇳🇪",
    "nf": "🇳🇫",
    "ng": "🇳🇬",
    "ni": "🇳🇮",
    "nl": "🇳🇱",
    "no": "🇳🇴",
    "np": "🇳🇵",
    "nr": "🇳🇷",
    "nu": "🇳🇺",
    "nz": "🇳🇿",
    "om": "🇴🇲",
    "pa": "🇵🇦",
    "pe": "🇵🇪",
    "pf": "🇵🇫",
    "pg": "🇵🇬",
    "ph": "🇵🇭",
    "pk": "🇵🇰",
    "pl": "🇵🇱",
    "pm": "🇵🇲",
    "pn": "🇵🇳",
    "pr": "🇵🇷",
    "ps": "🇵🇸",
    "pt": "🇵🇹",
    "pw": "🇵🇼",
    "py": "🇵🇾",
    "qa": "🇶🇦",
    "re": "🇷🇪",
    "ro": "🇷🇴",
    "rs": "🇷🇸",
    "ru": "🇷🇺",
    "rw": "🇷🇼",
    "sa": "🇸🇦",
    "sb": "🇸🇧",
    "sc": "🇸🇨",
    "sd": "🇸🇩",
    "se": "🇸🇪",
    "sg": "🇸🇬",
    "sh": "🇸🇭",
    "si": "🇸🇮",
    "sj": "🇸🇯",
    "sk": "🇸🇰",
    "sl": "🇸🇱",
    "sm": "🇸🇲",
    "sn": "🇸🇳",
    "so": "🇸🇴",
    "sr": "🇸🇷",
    "ss": "🇸🇸",
    "st": "🇸🇹",
    "sv": "🇸🇻",
    "sx": "🇸🇽",
    "sy": "🇸🇾",
    "sz": "🇸🇿",
    "tc": "🇹🇨",
    "td": "🇹🇩",
    "tf": "🇹🇫",
    "tg": "🇹🇬",
    "th": "🇹🇭",
    "tj": "🇹🇯",
    "tk": "🇹🇰",
    "tl": "🇹🇱",
    "tm": "🇹🇲",
    "tn": "🇹🇳",
    "to": "🇹🇴",
    "tr": "🇹🇷",
    "tt": "🇹🇹",
    "tv": "🇹🇻",
    "tw": "🇹🇼",
    "tz": "🇹🇿",
    "ua": "🇺🇦",
    "ug": "🇺🇬",
    "um": "🇺🇲",
    "us": "🇺🇸",
    "va": "🇻🇦",
    "vc": "🇻🇨",
    "ve": "🇻🇪",
    "vg": "🇻🇬",
    "vi": "🇻🇮",
    "vn": "🇻🇳",
    "vu": "🇻🇺",
    "wf": "🇼🇫",
    "ws": "🇼🇸",
    "xk": "🇽🇰",
    "ye": "🇾🇪",
    "yt": "🇾🇹",
    "za": "🇿🇦",
    "zm": "🇿🇲",
    "zw": "🇿🇼",
}