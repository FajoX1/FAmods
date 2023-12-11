#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: CodeBase64
# Description: Encode and decode base64
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/CodeBase64.png?raw=true
# ---------------------------------------------------------------------------------

import base64
import logging

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class CodeBase64(loader.Module):
    """Encode and decode base64"""

    strings = {
        "name": "CodeBase64",
        "enc_txt": "<b><emoji document_id=6334316848741352906>⌨️</emoji> You encoded text into base64:</b>\n<code>{}</code>",
        "de_txt": "<b><emoji document_id=6334316848741352906>⌨️</emoji> You decoded text from base64:</b>\n<code>{}</code>",
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
    async def cbase64(self, message):
        """Code into base64"""
        enc_bytes = base64.b64encode(utils.get_args_raw(message).encode('utf-8'))
        enc_text = enc_bytes

        await utils.answer(message, self.strings["enc_txt"].format(enc_text))

    @loader.command()
    async def dbase64(self, message):
        """Decode base64"""
        de_bytes = base64.b64decode(utils.get_args_raw(message))
        de_text = de_bytes

        await utils.answer(message, self.strings["de_txt"].format(de_text))