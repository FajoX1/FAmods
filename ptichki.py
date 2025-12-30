#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Ptichki
# Description: Генератор птиц
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/ptichki.png?raw=true
# requires: aiohttp pillow
# ---------------------------------------------------------------------------------

import json
import random
import aiohttp
import logging

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Ptichki(loader.Module):
    """Генератор птиц"""

    strings = {
        "name": "Ptichki",

        "no_args": "<emoji document_id=5314491961116232950>🦅</emoji> <b>Нужно </b><code>{}{} {}</code>",

        "generation": "<emoji document_id=5314482082691451962>🦅</emoji> <i>Генерирую птичку...</i>",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.assets_link = "https://github.com/fajox1/famods/raw/main/assets"

        self.font_url = f"{self.assets_link}/impact.ttf"
        self.birds_url = f"{self.assets_link}/birds/birds.json"
    
    async def fetch_bytes(self, url: str) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.read()
            
    async def get_bird_url(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.birds_url) as resp:
                birds_list = json.loads(await resp.text())
        
        return f"{self.assets_link}/birds/{random.choice(birds_list)}.png"

    async def generate_bird(self, text: str, format: str) -> bytes:

        text = text.upper()

        img_bytes = await self.fetch_bytes(
            await self.get_bird_url()
        )
        img = Image.open(BytesIO(img_bytes)).convert("RGBA")
        img.thumbnail((512, 512))
        width, height = img.size
        draw = ImageDraw.Draw(img)

        font_bytes = await self.fetch_bytes(self.font_url)
        font_size = 55
        min_font_size = 12
        max_width_fraction = 0.9

        font = ImageFont.truetype(BytesIO(font_bytes), font_size)
        text_width = font.getlength(text)

        if text_width > max_width_fraction * width:
            scale = (max_width_fraction * width) / text_width
            font_size = max(int(font_size * scale), min_font_size)
            font = ImageFont.truetype(BytesIO(font_bytes), font_size)

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) / 2
        y = height - text_height - (height * 0.05)

        draw.text(
            (x, y),
            text,
            font=font,
            fill="white",
            stroke_width=2,
            stroke_fill="black"
        )

        output = BytesIO()
        img.save(output, format=format.upper())
        output.seek(0)
        output.name = f"ptitchka.{format.lower()}"

        return output

    @loader.command()
    async def ptichka(self, message):
        """Сгенерировать стикер с птицей"""

        text = utils.get_args_raw(message)
        if not text:
            return await utils.answer(
                message, 
                self.strings["no_args"].format(
                    self.get_prefix(), "ptichka", "[текст]"
                )
            )

        m = await utils.answer(message, self.strings['generation'])

        await self.client.send_file(
            message.peer_id, 
            mime_type="image/webp",
            file=await self.generate_bird(text, format="webp"),
            reply_to=getattr(message.reply_to, "reply_to_msg_id", None),
        )

        return await m.delete()

    @loader.command()
    async def ptichka_img(self, message):
        """Сгенерировать фото с птицей"""

        text = utils.get_args_raw(message)
        if not text:
            return await utils.answer(
                message, 
                self.strings["no_args"].format(
                    self.get_prefix(), "ptichka_img", "[текст]"
                )
            )

        m = await utils.answer(message, self.strings['generation'])

        await self.client.send_file(
            message.peer_id, 
            mime_type="image/png",
            file=await self.generate_bird(text, format="png"),
            reply_to=getattr(message.reply_to, "reply_to_msg_id", None),
        )

        return await m.delete()