import re
import json

from zlib    import compress
from functools import partial
from typing import Optional
from inspect import isawaitable

from aiohttp import ClientSession
from asyncio import get_event_loop, AbstractEventLoop

from .response import PistonResponse
from .exceptions import ApiError

class AsyncMeta(type):

    async def __call__(self, *args, **kwargs):

        obb = object.__new__(self)
        fn  = obb.__init__(*args, **kwargs)

        if isawaitable(fn):
            await fn
        return obb

class Piston(metaclass=AsyncMeta):

    async def __init__(self, session: Optional[ClientSession] = None, loop: Optional[AbstractEventLoop] = None):
        self.API_URL       = "https://emkc.org/api/v1/piston/execute"
        self.LANGUAGES_URL = "https://emkc.org/api/v2/piston/runtimes"
        self.languages = []

        if loop:
            self.loop = loop
        else:
            self.loop = get_event_loop()
        
        if session:
            self.session = session
        else:
            self.session = ClientSession()

        await self._update_languages()

    async def __aenter__(self):
        self.session = ClientSession()
        await self._update_languages()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        await self.session.close()

    async def _update_languages(self):

        async with self.session.get(self.LANGUAGES_URL) as r:
            if r.ok:
                data = await r.json()
                self.languages = list(data.keys())
    
    async def execute(
        self, code: str, *, 
        language  : str, 
        inputs    : Optional[str] = "",
        compile_timeout: Optional[int] = 10000,
        run_timeout: Optional[int]  = 3000,
        arguments  : Optional[list] = [], 
    ):

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