#   █▀▀ ▄▀█   █▀▄▀█ █▀█ █▀▄ █▀
#   █▀░ █▀█   █░▀░█ █▄█ █▄▀ ▄█

#   https://t.me/famods

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# ---------------------------------------------------------------------------------
# Name: Cocoon [BETA]
# Description: Взаимодействие с Cocoon от HikkaHost
# meta developer: @FAmods & @vsecoder_m
# meta banner: https://github.com/FajoX1/FAmods/blob/main/assets/banners/cocoon.png?raw=true
# requires: openai httpx aiohttp
# ---------------------------------------------------------------------------------

import html
import httpx
import asyncio
import logging

from openai import AsyncOpenAI
from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

from telethon.errors import MessageNotModifiedError

from .. import loader, utils

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Usage:
    spent_nano: int
    spent_ton: str
    tokens_spent: int
    free_tokens_remaining: int
    free_tokens_reset_at: Optional[int]
    updated_at: Optional[int]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _safe_int(v: Any, default: int = 0) -> int:
    try:
        return int(v)
    except Exception:
        return default


def _escape_text(s: str) -> str:
    return html.escape(s or "", quote=False)


def _days_until_reset(reset_ts: Optional[int], cycle_days: int = 30) -> int:
    """
    Cocoon может отдавать free_tokens_reset_at как момент сброса текущего периода,
    который уже мог произойти сегодня. Тогда следующий сброс = reset_ts + cycle_days.
    """
    if not reset_ts:
        return cycle_days

    try:
        now = _now_utc()
        target = datetime.fromtimestamp(int(reset_ts), tz=timezone.utc)

        if target <= now:
            target = target + timedelta(days=cycle_days)

        delta = target - now
        if delta.total_seconds() <= 0:
            return 0

        return max(delta.days + (1 if delta.seconds > 0 else 0), 0)
    except Exception:
        return cycle_days


def _normalize_reset_ts(reset_at: Optional[int]) -> Optional[int]:
    if not reset_at:
        return None

    reset_at = _safe_int(reset_at, 0)
    if reset_at <= 0:
        return None

    return reset_at


def _format_compact(n: int) -> str:
    n = int(n)

    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}".rstrip("0").rstrip(".") + "b"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}".rstrip("0").rstrip(".") + "m"
    if n >= 1_000:
        return f"{n / 1_000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(n)


def _percent_remaining(spent: int, total: int) -> float:
    if total <= 0:
        return 0.0
    remaining = max(total - spent, 0)
    return (remaining / total) * 100.0


@loader.tds
class Cocoon(loader.Module):
    """Взаимодействие с Cocoon от HikkaHost"""

    strings = {
        "name": "Cocoon [BETA]",
        "try_again": "<emoji document_id=5456307331644037599>❌</emoji> <b>Что-то пошло не так. Попробуйте снова.</b>",
        "no_args": "<emoji document_id=5456307331644037599>❌</emoji> <b>Нужно </b><code>{}{} {}</code>",
        "no_token": "<emoji document_id=5456307331644037599>❌</emoji> <b>Нету токена! Вставь его в <code>{}cfg cocoon</code>",
        "invalid_token_or_no_sub": (
            "<b><emoji document_id=5456307331644037599>❌</emoji>Неверный токен или у вас нет подписки <emoji document_id=5188377234380954537>🌘</emoji> HikkaHost.</b>\n\n"
            "<emoji document_id=5456672880605565619>🌘</emoji> Получить токен: @hikkahost_bot → <emoji document_id=5208521532942358129>🥚</emoji> Cocoon</b>"
        ),
        "sending_request_to_cocoon": "<emoji document_id=5197252827247841976>🐣</emoji> <b>Отправляю запрос к Cocoon...</b>",
        "thinking": (
            "<emoji document_id=5197252827247841976>🐣</emoji> <b>Думаю...</b>\n\n"
            "<blockquote>{thoughts}…</blockquote>"
        ),
        "answer": (
            "<emoji document_id=5456217626957091223>🌘</emoji> <b>Вопрос:</b> {question}\n\n"
            "<emoji document_id=5197252827247841976>🐣</emoji> <b>Размышления:</b>\n"
            "<blockquote expandable>{thoughts}</blockquote>\n\n"
            "<emoji document_id=5208521532942358129>🥚</emoji> {answer}\n\n"
            "<emoji document_id=5458567764341985638>🚀</emoji> <b>Модель</b>: <code>{model}</code>"
        ),
        "usage": (
            "<b><emoji document_id=5208521532942358129>🥚</emoji> Cocoon API\n\n"
            "<emoji document_id=5458805877328875335>💡</emoji> Использовано:\n"
            "</b><i>• {current}/{total} ({percent}% осталось)</i><b>\n\n"
            "<emoji document_id=5456591761558245861>⏳</emoji> Лимит сбросится через {days} день(-ей).</b>"
        ),
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                lambda: "Токен HikkaHost API. Получить токен: @hikkahost_bot -> 🥚 Cocoon",
                validator=loader.validators.Hidden(loader.validators.String()),
            ),
            loader.ConfigValue(
                "model",
                "Qwen/Qwen3-32B",
                lambda: "Модель ИИ. Список: https://cocoon.hikka.host/v1/models",
            ),
            loader.ConfigValue(
                "role",
                "user",
                lambda: "Роль user-сообщения (обычно user).",
            ),
            loader.ConfigValue(
                "system_prompt",
                "",
                lambda: "System prompt (инструкция для модели, role=system).",
            ),
            loader.ConfigValue(
                "max_tokens",
                3900,
                lambda: "Максимальное количество токенов для ответа модели.",
                validator=loader.validators.Integer(minimum=1),
            ),
            loader.ConfigValue(
                "temperature",
                0.2,
                lambda: "Температура генерации (0.0–1.0).",
            ),
        )

    async def client_ready(self, client, db):
        self.db = db
        self._client = client

        self.api_url = "https://cocoon.hikka.host/v1"
        self._openai: Optional[AsyncOpenAI] = None

    def _rebuild_openai_client(self) -> None:
        token = self.config.get("token") or ""
        self._openai = AsyncOpenAI(
            api_key=token, base_url=self.api_url, timeout=60.0, max_retries=2
        )

    def _ensure_client(self) -> None:
        if not self._openai or (
            self._openai.api_key != (self.config.get("token") or "")
        ):
            self._rebuild_openai_client()

    async def _answer(self, message, text):
        try:
            if len(text) > 4096:
                text = text[:4090] + "..."
            return await utils.answer(message, text)
        except MessageNotModifiedError:
            return message

    async def _fetch_usage(self) -> Optional[Usage]:
        token = self.config.get("token")
        if not token:
            return None

        headers = {
            "accept": "application/json",
            "X-API-Key": token,
        }

        try:
            async with httpx.AsyncClient(timeout=20.0) as client:
                r = await client.get(f"{self.api_url}/usage", headers=headers)
                r.raise_for_status()
                data = r.json()
        except Exception as e:
            logger.exception("Usage request failed: %s", e)
            return None

        if isinstance(data, dict) and data.get("detail") == "API key not recognized":
            return None

        if not isinstance(data, dict):
            return None

        return Usage(
            spent_nano=_safe_int(data.get("spent_nano"), 0),
            spent_ton=str(data.get("spent_ton", "0")),
            tokens_spent=_safe_int(data.get("tokens_spent"), 0),
            free_tokens_remaining=_safe_int(data.get("free_tokens_remaining"), 0),
            free_tokens_reset_at=(
                _safe_int(data.get("free_tokens_reset_at"), 0) or None
            ),
            updated_at=(_safe_int(data.get("updated_at"), 0) or None),
        )

    @loader.command()
    async def ccusage(self, message):
        """Статистика использования Cocoon"""

        if not self.config.get("token"):
            return await self._answer(
                message, self.strings["no_token"].format(self.get_prefix())
            )

        usage = await self._fetch_usage()
        if not usage:
            return await self._answer(message, self.strings["invalid_token_or_no_sub"])

        reset_ts = _normalize_reset_ts(usage.free_tokens_reset_at)
        days = _days_until_reset(reset_ts, cycle_days=30)

        spent = usage.tokens_spent
        total = spent + usage.free_tokens_remaining
        if total <= 0:
            total = 1_000_000

        percent = _percent_remaining(spent, total)
        percent_fmt = f"{percent:.1f}".rstrip("0").rstrip(".")

        return await self._answer(
            message,
            self.strings["usage"].format(
                current=_format_compact(spent),
                total=_format_compact(total),
                percent=percent_fmt,
                days=days,
            ),
        )

    @loader.command()
    async def cocoon(self, message):
        """Задать вопрос к ИИ"""

        q = utils.get_args_raw(message)
        if not q:
            return await utils.answer(
                message,
                self.strings["no_args"].format(self.get_prefix(), "cocoon", "[вопрос]"),
            )

        if not self.config["token"]:
            return await utils.answer(
                message, self.strings["no_token"].format(self.get_prefix())
            )

        usage = await self._fetch_usage()
        if not usage:
            return await utils.answer(message, self.strings["invalid_token_or_no_sub"])

        message = await utils.answer(message, self.strings["sending_request_to_cocoon"])

        self._ensure_client()

        client = AsyncOpenAI(api_key=self.config["token"], base_url=self.api_url)

        system_prompt = (self.config.get("system_prompt") or "").strip()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": self.config["role"] or "user", "content": q})

        try:
            response = await client.chat.completions.create(
                messages=messages,
                stream=True,
                max_tokens=self.config.get("max_tokens", 3900),
                model=self.config.get("model", "Qwen/Qwen3-32B"),
                temperature=self.config.get("temperature", 0.2)
            )

            response_text = ""
            chunk_buffer = ""

            async for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    chunk_buffer += chunk.choices[0].delta.content

                if len(chunk_buffer) >= 150:
                    response_text += chunk_buffer
                    chunk_buffer = ""

                    thoughts = (
                        response_text.replace("<think>", "")
                        .replace("</think>", "")
                        .strip()
                    )

                    if "</think>" in response_text:
                        after_think = response_text.split("</think>", 1)[-1].strip()
                        await self._answer(
                            message,
                            self.strings["answer"].format(
                                thoughts=thoughts[:300],
                                question=q,
                                answer=_escape_text(after_think) + "…",
                                model=self.config["model"],
                            ),
                        )
                    else:
                        thinking_text = (
                            response_text.replace("<think>", "")
                            .replace("</think>", "")
                            .strip()
                        )
                        await self._answer(
                            message,
                            self.strings["thinking"].format(
                                thoughts=_escape_text(thinking_text)
                            ),
                        )

                    await asyncio.sleep(2)

            if chunk_buffer:
                response_text += chunk_buffer

            if "</think>" in response_text:
                after_think = response_text.split("</think>", 1)[-1].strip()
            else:
                after_think = (
                    response_text.replace("<think>", "").replace("</think>", "").strip()
                )

            await self._answer(
                message,
                self.strings["answer"].format(
                    thoughts=thoughts,
                    question=q,
                    answer=_escape_text(after_think),
                    model=self.config["model"],
                ),
            )

        except httpx.RemoteProtocolError:
            return await self._answer(message, self.strings["try_again"])
