#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: AutoGH
# Description: Авто-коммиты в Github
# meta developer: @FAmods
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/autogh.png?raw=true
# requires: PyGithub
# ---------------------------------------------------------------------------------

import asyncio
import logging

from github import Github
from datetime import datetime

from telethon.tl.functions.channels import JoinChannelRequest

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class AutoGH(loader.Module):
    """Авто-коммиты в Github"""

    strings = {
        "name": "AutoGH",

        "no_cfg": "<b><emoji document_id=5854929766146118183>🚫</emoji> Нету {}! Вставьте его в config через <code>{}cfg AutoGH</code></b>",

        "autocommit_on": "<b><emoji document_id=4985961065012527769>🖥</emoji> Авто-коммит включен!</b>",
        "autocommit_off": "<b><emoji document_id=5854929766146118183>🚫</emoji> Авто-коммит выключен!</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "API_TOKEN",
                None,
                lambda: "Github API Token. Создать токен можно в https://github.com/settings/tokens/new",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "REPO",
                None,
                lambda: "Репозиторий для авто-коммитов. Пример: FajoX1/FAmods",
            ),
            loader.ConfigValue(
                "time_autocommit",
                3600,
                lambda: "Через сколько секунд сделать следущий коммит",
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

        asyncio.create_task(self._autocommit())

    async def _autocommit(self):
      while True:
        if self.db.get(self.name, "autocommit", False):
            try:
                g = Github(self.config['API_TOKEN'])
                repo = g.get_repo(self.config['REPO'])
                file_name = f'autocommit.txt'
                file_content = f'Commit at {datetime.now()}'
                contents = repo.get_contents(file_name)
                sha = contents.sha
                repo.update_file(file_name, "AutoCommit", file_content, sha)
                logger.info("Auto commited")
            except Exception as e:
                logger.error(f"Can't commit:\n{e}")
        
        await asyncio.sleep(self.config['time_autocommit'])

    @loader.command()
    async def autocommit(self, message):
        """Включить/выключить автоматический коммит"""

        if not self.config['API_TOKEN']:
            return await utils.answer(message, self.strings['no_cfg'].format("токена github", self.get_prefix()))
        
        if not self.config['REPO']:
            return await utils.answer(message, self.strings['no_cfg'].format("названия репозитория", self.get_prefix()))

        if self.db.get(self.name, "autocommit", False):
            self.db.set(self.name, "autocommit", False)
            return await utils.answer(message, self.strings["autocommit_off"])

        self.db.set(self.name, "autocommit", True)

        await utils.answer(message, self.strings["autocommit_on"])