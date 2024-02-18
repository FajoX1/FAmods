#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Requirements
# Description: Работа с pip пакетами в модуле
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/requirements.png?raw=true
# requires: aiohttp
# ---------------------------------------------------------------------------------

import re
import os
import shlex
import asyncio
import aiohttp
import logging
import tempfile

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class Requirements(loader.Module):
    """Работа с pip пакетами в модуле"""

    strings = {
        "name": "Requirements",

        "no_dep": "<emoji document_id=5440381017384822513>❌</emoji> <b>В модуле нету зависимостей</b>",
        "only_url": "<emoji document_id=5440381017384822513>❌</emoji> <b>Только ссылка на модуль</b>",

        "no_file_and_link": "<emoji document_id=5440381017384822513>❌</emoji> <b>Нужно ответить на файл или <code>{}{} [ссылка]</code></b>",

        "search_deps": "<emoji document_id=6332573220868196043>🕓</emoji> <b>Ищу зависимости...</b>",
        "install_deps": "<emoji document_id=6332573220868196043>🕓</emoji> <b>Установка зависимостей:</b>\n\n<code>{}</code>",
        "uninstall_deps": "<emoji document_id=6332573220868196043>🕓</emoji> <b>Удаление зависимостей:</b>\n\n<code>{}</code>",

        "installed": "<emoji document_id=5021905410089550576>✅</emoji> <b>Успешно установил зависимости:</b>\n\n<code>{}</code>\n\n{}",
        "uninstalled": "<emoji document_id=5021905410089550576>✅</emoji> <b>Успешно удалил зависимости:</b>\n\n<code>{}</code>",

        "requirements": "<emoji document_id=5294080842006538030>⚙️</emoji> <b>Зависимости:</b>\n\n<code>{}</code>",
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
    async def dldeps(self, message):
        """Установить pip пакеты с модуля"""
        
        link = utils.get_args_raw(message)

        r = await message.get_reply_message()

        if not link and not r:
            return await utils.answer(message, self.strings['no_file_and_link'].format(self.get_prefix(), "dldeps"))

        await utils.answer(message, self.strings['search_deps'])

        if link:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as response:
                        code = await response.text()
            except:
                return await utils.answer(message, self.strings['only_url'])
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, r.file.name)
                await r.download_media(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

        requires_comments = re.findall(r'#\s*requires:\s*(.*)', code)

        all_requires = ''.join(requires_comments).strip()

        if not all_requires:
            return await utils.answer(message, self.strings['no_dep'])

        await utils.answer(message, self.strings['install_deps'].format(all_requires.replace(" ", "\n")))

        requirements_list = shlex.split(all_requires)

        process = await asyncio.create_subprocess_exec('pip', 'install', *requirements_list)
        await process.wait()

        return await utils.answer(message, self.strings['installed'].format(all_requires.replace(" ", "\n"), f"<b><emoji document_id=6334353510582191829>⬇️</emoji> Установите модуль:\n<code>{self.get_prefix()}dlmod {link}</code></b>" if link else f"<b><emoji document_id=6334353510582191829>⬇️</emoji> Установите модуль через <code>{self.get_prefix()}lm</code> (с ответом на файл модуля)</b>"))

    @loader.command()
    async def uldeps(self, message):
        """Удалить pip пакеты с модуля"""
        
        link = utils.get_args_raw(message)

        r = await message.get_reply_message()

        if not link and not r:
            return await utils.answer(message, self.strings['no_file_and_link'].format(self.get_prefix(), "uldeps"))

        await utils.answer(message, self.strings['search_deps'])

        if link:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as response:
                        code = await response.text()
            except:
                return await utils.answer(message, self.strings['only_url'])
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, r.file.name)
                await r.download_media(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

        requires_comments = re.findall(r'#\s*requires:\s*(.*)', code)

        all_requires = ''.join(requires_comments).strip()

        if not all_requires:
            return await utils.answer(message, self.strings['no_dep'])

        await utils.answer(message, self.strings['uninstall_deps'].format(all_requires.replace(" ", "\n")))

        requirements_list = shlex.split(all_requires)

        process = await asyncio.create_subprocess_exec('pip', 'uninstall', *requirements_list, '-y')
        await process.wait()

        return await utils.answer(message, self.strings['uninstalled'].format(all_requires.replace(" ", "\n")))
    
    @loader.command()
    async def deps(self, message):
        """Посмотреть pip пакеты с модуля"""
        
        link = utils.get_args_raw(message)

        r = await message.get_reply_message()

        if not link and not r:
            return await utils.answer(message, self.strings['no_file_and_link'].format(self.get_prefix(), "deps"))

        await utils.answer(message, self.strings['search_deps'])

        if link:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as response:
                        code = await response.text()
            except:
                return await utils.answer(message, self.strings['only_url'])
        else:
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, r.file.name)
                await r.download_media(file_path)
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()

        requires_comments = re.findall(r'#\s*requires:\s*(.*)', code)

        all_requires = ''.join(requires_comments).strip()

        if not all_requires:
            return await utils.answer(message, self.strings['no_dep'])

        return await utils.answer(message, self.strings['requirements'].format(all_requires.replace(" ", "\n"), f"<b><emoji document_id=6334353510582191829>⬇️</emoji> Модуль: <code>{link}</code>"))
