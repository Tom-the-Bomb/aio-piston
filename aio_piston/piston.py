from __future__ import annotations

import json
import asyncio

from typing import Optional

from aiohttp import ClientSession

from .response import PistonResponse
from .exceptions import ApiError

class Piston:

    def __init__(
        self, 
        session: Optional[ClientSession] = None, 
        loop: Optional[asyncio.AbstractEventLoop] = None, *,
        store_languages: Optional[bool] = True,
    ) -> None:

        self._store_languages = store_languages
        self.API_URL = "https://emkc.org/api/v1/piston/execute"
        self.LANGUAGES_URL = "https://emkc.org/api/v2/piston/runtimes"
        self.languages = []

        if loop:
            self.loop = loop
        else:
            try:
                self.loop = asyncio.get_running_loop()
            except RuntimeError:
                self.loop = asyncio.get_event_loop()
        
        if session:
            self.session = session
        else:
            self.session = None

        if self.loop.is_running():
            self.loop.create_task(self._update_languages())
        else:
            self.loop.run_until_complete(self._update_languages())

    async def __aenter__(self) -> Piston:
        await self._update_languages()
        return self

    async def __aexit__(self, *_) -> None:
        await self.close()

    async def close(self) -> None:
        await self.session.close()

    async def _update_languages(self) -> None:
        self.session = ClientSession()
        if self._store_languages:
            async with self.session.get(self.LANGUAGES_URL) as r:
                if r.ok:
                    data = await r.json()
                    self.languages = [item.get("language", "N/A") for item in data]
        return None
    
    async def execute(
        self, code: str, *, 
        language  : str, 
        inputs    : Optional[str] = "",
        compile_timeout: Optional[int] = 10000,
        run_timeout: Optional[int]  = 3000,
        arguments  : Optional[list] = [], 
    ) -> Optional[PistonResponse]:

        data = json.dumps({
            "language": language,
            "source"  : code,
            "stdin"   : inputs,
            "compile_timeout": compile_timeout,
            "run_timeout": run_timeout,
            "args"       : arguments,
        })

        async with self.session.post(self.API_URL, data=data) as r:

            data = await r.json()
            if r.ok:
                return PistonResponse(data)
            else:
                raise ApiError(f"Error {r.status} {data.get('message', r.reason)}")